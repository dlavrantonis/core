"""Interfaces with  alarm control panels."""
import logging


import voluptuous as vol

from homeassistant.components.alarm_control_panel import (
    PLATFORM_SCHEMA,
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
)
from homeassistant.components.guarddionisis.util.util import DBAccess
from homeassistant.const import (
    CONF_ID,
    CONF_NAME,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "guarddionisis"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_ID): cv.positive_int,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up a nightwatvhman control panel."""
    name = config.get(CONF_NAME)
    id = config.get(CONF_ID)
    guard = GuardAlarmEntity(hass, name, id)
    async_add_entities([guard])



class GuardAlarmEntity(AlarmControlPanelEntity):
    """Representation of an Alarm.com status."""
    
    _attr_code_arm_required = False

    def __init__(self, hass, name, id):
        """Initialize the Alarm.com status."""
        self.theDB = DBAccess('Database/TrackedObjectsDim.db')
        _LOGGER.debug("Setting up dionisisalarm...")
        self._hass = hass
        self._name = name
        self._id = id
        
        if self.theDB.conn and id is not None:
            db_state = self.theDB.getAlarmState(id)
            try:
                self._attr_alarm_state = AlarmControlPanelState(db_state) if db_state else AlarmControlPanelState.DISARMED
            except ValueError:
                self._attr_alarm_state = AlarmControlPanelState.DISARMED
        else:
            self._attr_alarm_state = AlarmControlPanelState.DISARMED

    async def async_update(self):
        """Fetch the latest state."""
        if self.theDB.conn and self._id:
            db_state = self.theDB.getAlarmState(self._id)
            if db_state:
                try:
                    self._attr_alarm_state = AlarmControlPanelState(db_state)
                except ValueError:
                    pass

    @property
    def name(self):
        """Return the name of the alarm."""
        return self._name

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return (
            AlarmControlPanelEntityFeature.ARM_HOME
            | AlarmControlPanelEntityFeature.ARM_AWAY
            | AlarmControlPanelEntityFeature.ARM_NIGHT
            | AlarmControlPanelEntityFeature.TRIGGER
        )

    async def async_alarm_disarm(self, code=None):
        """Send disarm command."""
        if not self.theDB.conn:
            return
        if await self.theDB.Disarm(self._id):
            self._attr_alarm_state = AlarmControlPanelState.DISARMED
            await self.theDB.setAlarmState(self._id, self._attr_alarm_state.value)
            # self.async_write_ha_state()

    async def async_alarm_arm_home(self, code=None):
        """Send arm home command."""
        if not self.theDB.conn:
            return
        if await self.theDB.ArmHome(self._id):
            self._attr_alarm_state = AlarmControlPanelState.ARMED_HOME
            await self.theDB.setAlarmState(self._id, self._attr_alarm_state.value)
            # self.async_write_ha_state()

    async def async_alarm_arm_away(self, code=None):
        """Send arm away command."""
        if not self.theDB.conn:
            return
        if await self.theDB.ArmAway(self._id):
            self._attr_alarm_state = AlarmControlPanelState.ARMED_AWAY
            await self.theDB.setAlarmState(self._id, self._attr_alarm_state.value)
            # self.async_write_ha_state()

    async def async_alarm_arm_night(self, code=None):
        """Send arm night command."""
        if not self.theDB.conn:
            return
        if await self.theDB.ArmNight(self._id):
            self._attr_alarm_state = AlarmControlPanelState.ARMED_NIGHT
            await self.theDB.setAlarmState(self._id, self._attr_alarm_state.value)
            # self.async_write_ha_state()

    async def async_alarm_trigger(self, code=None):
        """Send alarm trigger command."""
        if not self.theDB.conn:
            return
        if await self.theDB.Disarm(self._id):
            self._attr_alarm_state = AlarmControlPanelState.TRIGGERED
            await self.theDB.setAlarmState(self._id, self._attr_alarm_state.value)
            # self.async_write_ha_state()

    async def async_alarm_day(self, code=None):
        """Send arm day command."""
        if not self.theDB.conn:
            return
        if await self.theDB.ArmDay(self._id):
            self._attr_alarm_state = AlarmControlPanelState.ARMED_HOME
            await self.theDB.setAlarmState(self._id, self._attr_alarm_state.value)
            # self.async_write_ha_state()