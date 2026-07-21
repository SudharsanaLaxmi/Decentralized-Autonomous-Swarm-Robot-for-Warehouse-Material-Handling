"""
Gateway server for robot communication

Provides central communication hub for robot swarm with:
- UDP network interface
- Message routing and relaying
- Telemetry collection
- Command distribution
"""

import socket
import threading
import logging
from typing import Dict, Tuple, Optional
from queue import Queue
import time

from communication.protocol.messages import Message, MessageType
from communication.protocol.robot_id import RobotRegistry, RobotIdentity, RobotType

logger = logging.getLogger(__name__)


class GatewayServer:
    """
    Central communication gateway for robot swarm.
    
    Receives messages from robots, routes, and relays commands.
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8888,
                 buffer_size: int = 1024):
        """
        Initialize gateway server.
        
        Args:
            host: Bind address (0.0.0.0 for all interfaces)
            port: UDP port number
            buffer_size: Receive buffer size in bytes
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.registry = RobotRegistry()
        
        # Message queues
        self.rx_queue: Queue = Queue()      # Inbound messages
        self.tx_queue: Queue = Queue()      # Outbound messages
        
        # Robot address mapping
        self.robot_addresses: Dict[int, Tuple[str, int]] = {}
        
        # Statistics
        self.stats = {
            'messages_received': 0,
            'messages_sent': 0,
            'errors': 0,
            'uptime_seconds': 0,
        }
        self.start_time = None
    
    def start(self) -> bool:
        """
        Start gateway server.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.host, self.port))
            self.socket.settimeout(1.0)
            
            self.running = True
            self.start_time = time.time()
            
            logger.info(f"Gateway listening on {self.host}:{self.port}")
            
            # Start receiver thread
            self.rx_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.rx_thread.start()
            
            # Start transmitter thread
            self.tx_thread = threading.Thread(target=self._transmit_loop, daemon=True)
            self.tx_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start gateway: {e}")
            self.stats['errors'] += 1
            return False
    
    def stop(self) -> None:
        """Stop gateway server."""
        self.running = False
        if self.socket:
            self.socket.close()
        logger.info("Gateway stopped")
    
    def _receive_loop(self) -> None:
        """Receive messages from robots."""
        while self.running:
            try:
                data, addr = self.socket.recvfrom(self.buffer_size)
                
                message = Message.deserialize(data)
                if message:
                    self.robot_addresses[message.robot_id] = addr
                    self.rx_queue.put((message, addr))
                    self.stats['messages_received'] += 1
                    
                    logger.debug(f"RX: {message.msg_type} from robot {message.robot_id}")
                    
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Receive error: {e}")
                self.stats['errors'] += 1
    
    def _transmit_loop(self) -> None:
        """Transmit messages to robots."""
        while self.running:
            try:
                if self.tx_queue.empty():
                    time.sleep(0.01)
                    continue
                
                message, robot_id = self.tx_queue.get(timeout=1.0)
                
                if robot_id not in self.robot_addresses:
                    logger.warning(f"No address for robot {robot_id}")
                    continue
                
                addr = self.robot_addresses[robot_id]
                data = message.serialize()
                
                self.socket.sendto(data, addr)
                self.stats['messages_sent'] += 1
                
                logger.debug(f"TX: {message.msg_type} to robot {robot_id}")
                
            except Exception as e:
                logger.error(f"Transmit error: {e}")
                self.stats['errors'] += 1
    
    def send_to_robot(self, message: Message, robot_id: int) -> bool:
        """
        Queue message for transmission to robot.
        
        Args:
            message: Message to send
            robot_id: Target robot ID
            
        Returns:
            True if queued successfully
        """
        try:
            self.tx_queue.put((message, robot_id), timeout=1.0)
            return True
        except Exception as e:
            logger.error(f"Failed to queue message: {e}")
            return False
    
    def get_telemetry(self, timeout: float = 0.1) -> Optional[Message]:
        """
        Retrieve oldest telemetry message from queue.
        
        Args:
            timeout: Maximum wait time
            
        Returns:
            Message or None if queue empty
        """
        try:
            message, addr = self.rx_queue.get(timeout=timeout)
            return message
        except:
            return None
    
    def get_statistics(self) -> Dict:
        """Get gateway statistics."""
        if self.start_time:
            self.stats['uptime_seconds'] = time.time() - self.start_time
        
        self.stats.update(self.registry.get_swarm_status())
        return self.stats
    
    def register_robot(self, identity: RobotIdentity) -> bool:
        """Register robot with gateway."""
        return self.registry.register_robot(identity)


# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    gateway = GatewayServer(host='0.0.0.0', port=8888)
    gateway.start()
    
    try:
        while True:
            msg = gateway.get_telemetry(timeout=1.0)
            if msg:
                logger.info(f"Telemetry from robot {msg.robot_id}")
            
            stats = gateway.get_statistics()
            if gateway.stats['messages_received'] % 100 == 0:
                logger.info(f"Stats: {stats}")
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        gateway.stop()
