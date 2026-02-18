import json
from datetime import datetime
from typing import Set
import asyncio

class WebSocketMonitor:
    """
    Real-time WebSocket monitoring for risk detection updates
    """
    def __init__(self):
        self.active_connections: Set = set()
        self.message_queue = asyncio.Queue()
    
    async def connect(self, websocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"✅ Client connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket):
        """Handle WebSocket disconnection"""
        self.active_connections.discard(websocket)
        print(f"❌ Client disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.active_connections.discard(conn)
    
    async def send_realtime_update(self, risk_data: dict):
        """
        Send real-time risk updates to all connected clients
        
        Args:
            risk_data: Dictionary containing risk analysis results
        """
        update = {
            'timestamp': datetime.now().isoformat(),
            'type': 'risk_update',
            'risk_score': risk_data.get('risk_score', 0),
            'risk_level': self.get_risk_level(risk_data.get('risk_score', 0)),
            'reason': risk_data.get('reason', 'Unknown risk'),
            'content_type': risk_data.get('content_type', 'Unknown'),
            'detected_risks': risk_data.get('detected_risks', []),
            'recommendations': self.get_recommendations(risk_data)
        }
        
        await self.broadcast(update)
    
    async def send_alert(self, risk_data: dict):
        """Send critical alert to all clients"""
        if risk_data.get('risk_score', 0) >= 70:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'type': 'critical_alert',
                'severity': 'CRITICAL' if risk_data.get('risk_score', 0) >= 90 else 'HIGH',
                'risk_score': risk_data.get('risk_score'),
                'reason': risk_data.get('reason'),
                'action_required': True
            }
            await self.broadcast(alert)
    
    async def send_stats_update(self, stats: dict):
        """Send monitoring statistics update"""
        update = {
            'timestamp': datetime.now().isoformat(),
            'type': 'stats_update',
            'total_scans': stats.get('total_scans'),
            'average_risk_score': stats.get('average_risk_score'),
            'high_risk_count': stats.get('high_risk_count'),
            'last_scan_time': stats.get('last_scan_time')
        }
        await self.broadcast(update)
    
    @staticmethod
    def get_risk_level(score: float) -> str:
        """
        Get risk level name based on score
        
        Args:
            score: Risk score 0-100
            
        Returns:
            Risk level name (CRITICAL, HIGH, MEDIUM, LOW)
        """
        if score >= 80:
            return 'CRITICAL'
        elif score >= 60:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def get_recommendations(risk_data: dict) -> list:
        """
        Get security recommendations based on risk type
        
        Args:
            risk_data: Risk analysis data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        risk_level = WebSocketMonitor.get_risk_level(risk_data.get('risk_score', 0))
        detected_risks = risk_data.get('detected_risks', [])
        
        if 'MALWARE' in detected_risks:
            recommendations.append('⚠️ Run antivirus scan immediately')
            recommendations.append('🔒 Isolate affected system from network')
            recommendations.append('📋 Review file execution history')
        
        if 'PHISHING' in detected_risks:
            recommendations.append('🚫 Do not click on links or submit forms')
            recommendations.append('📧 Verify sender identity through official channels')
            recommendations.append('🔔 Report to security team')
        
        if 'SUSPICIOUS_LINKS' in detected_risks:
            recommendations.append('🔍 Verify URL destination before clicking')
            recommendations.append('✅ Use URL checker tools')
            recommendations.append('🛡️ Enable link preview before visiting')
        
        if 'EXPLICIT_CONTENT' in detected_risks:
            recommendations.append('🚫 Block content source')
            recommendations.append('📋 Document incident')
            recommendations.append('👀 Report to appropriate authorities if needed')
        
        if 'INJECTION_ATTACK' in detected_risks:
            recommendations.append('🔐 Sanitize all user inputs')
            recommendations.append('🛡️ Use parameterized queries')
            recommendations.append('📊 Update WAF rules')
        
        if 'DATA_EXFILTRATION' in detected_risks:
            recommendations.append('⏸️ Stop all processes immediately')
            recommendations.append('🔒 Revoke compromised credentials')
            recommendations.append('📍 Trace data access patterns')
        
        if risk_level == 'CRITICAL':
            recommendations.insert(0, '🚨 CRITICAL: Contact security team immediately')
        elif risk_level == 'HIGH':
            recommendations.insert(0, '⚠️ HIGH RISK: Take immediate action')
        
        return recommendations
    
    def get_connection_count(self) -> int:
        """Get number of active WebSocket connections"""
        return len(self.active_connections)