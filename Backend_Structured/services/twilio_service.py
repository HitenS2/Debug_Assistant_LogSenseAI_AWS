"""
Twilio Service - Manages alert delivery via SMS, Voice, and WhatsApp
"""

import asyncio
import structlog

from models import Alert
from config import settings

logger = structlog.get_logger()


class TwilioService:
    """
    Manages alert delivery through Twilio:
    - SMS alerts
    - Voice call alerts
    - WhatsApp alerts
    - Escalation workflows
    """
    
    def __init__(self):
        # Placeholder for Twilio client
        # In production: from twilio.rest import Client
        # self.client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        self.client = None
        self.from_number = settings.twilio_phone_number
        self.oncall_number = settings.oncall_phone_number
        self.oncall_whatsapp = settings.oncall_whatsapp_number
    
    async def send_alert(self, alert: Alert):
        """
        Send alert via multiple channels based on severity
        
        - MEDIUM/HIGH: SMS only
        - CRITICAL: SMS + WhatsApp + Voice call (if not acknowledged)
        """
        logger.info(
            "sending_alert",
            alert_id=alert.alert_id,
            service=alert.service,
            severity=alert.severity
        )
        
        # Always send SMS
        await self._send_sms(alert)
        
        # For critical alerts, use multiple channels
        if alert.severity == "CRITICAL":
            await self._send_whatsapp(alert)
            
            # Wait 1 minute, then make voice call if not acknowledged
            await asyncio.sleep(60)
            
            if not await self._is_acknowledged(alert.alert_id):
                await self._make_voice_call(alert)
        
        logger.info(
            "alert_sent",
            alert_id=alert.alert_id,
            severity=alert.severity
        )
    
    async def _send_sms(self, alert: Alert):
        """Send SMS alert"""
        
        message_body = f"""🚨 ALERT: {alert.service}

Warning Count: {alert.warning_count}
Time Window: {alert.time_window}
Severity: {alert.severity}

Action: {alert.suggested_action}

Alert ID: {alert.alert_id}
Time: {alert.timestamp}
"""
        
        logger.info(
            "sending_sms",
            alert_id=alert.alert_id,
            to=self.oncall_number
        )
        
        # Placeholder for actual Twilio SMS API call
        # message = self.client.messages.create(
        #     to=self.oncall_number,
        #     from_=self.from_number,
        #     body=message_body
        # )
        
        logger.info(
            "sms_sent",
            alert_id=alert.alert_id,
            # message_sid=message.sid
        )
    
    async def _send_whatsapp(self, alert: Alert):
        """Send WhatsApp alert"""
        
        message_body = f"""🚨 CRITICAL ALERT: {alert.service}

⚠️ Warning Count: {alert.warning_count}
⏱️ Time Window: {alert.time_window}
🔴 Severity: {alert.severity}

📋 Action Required:
{alert.suggested_action}

🆔 Alert ID: {alert.alert_id}
🕐 Time: {alert.timestamp}

Please acknowledge this alert immediately.
"""
        
        logger.info(
            "sending_whatsapp",
            alert_id=alert.alert_id,
            to=self.oncall_whatsapp
        )
        
        # Placeholder for actual Twilio WhatsApp API call
        # message = self.client.messages.create(
        #     to=self.oncall_whatsapp,
        #     from_=f'whatsapp:{self.from_number}',
        #     body=message_body
        # )
        
        logger.info(
            "whatsapp_sent",
            alert_id=alert.alert_id
        )
    
    async def _make_voice_call(self, alert: Alert):
        """Make voice call alert"""
        
        # TwiML for voice message
        twiml_message = f"""
        <Response>
            <Say voice="alice">
                Critical alert for {alert.service}.
                Warning count is {alert.warning_count} in the last {alert.time_window}.
                Immediate action required.
                Alert ID: {alert.alert_id}.
                Press 1 to acknowledge this alert.
            </Say>
            <Gather numDigits="1" action="/alert/acknowledge/{alert.alert_id}">
                <Say>Press 1 to acknowledge.</Say>
            </Gather>
        </Response>
        """
        
        logger.info(
            "making_voice_call",
            alert_id=alert.alert_id,
            to=self.oncall_number
        )
        
        # Placeholder for actual Twilio Voice API call
        # call = self.client.calls.create(
        #     to=self.oncall_number,
        #     from_=self.from_number,
        #     twiml=twiml_message
        # )
        
        logger.info(
            "voice_call_initiated",
            alert_id=alert.alert_id
        )
    
    async def _is_acknowledged(self, alert_id: str) -> bool:
        """
        Check if alert has been acknowledged
        
        In production, this would check a database or cache
        """
        # Placeholder for acknowledgment check
        return False
    
    async def send_escalated_alert(self, alert: Alert):
        """
        Send escalated alert to secondary contacts
        
        Uses all channels immediately
        """
        logger.warning(
            "sending_escalated_alert",
            alert_id=alert.alert_id,
            service=alert.service
        )
        
        # Send to primary contact
        await self._send_sms(alert)
        await self._send_whatsapp(alert)
        await self._make_voice_call(alert)
        
        # TODO: Send to secondary contacts
        # await self._send_to_secondary_contacts(alert)
        
        logger.warning(
            "escalated_alert_sent",
            alert_id=alert.alert_id
        )
