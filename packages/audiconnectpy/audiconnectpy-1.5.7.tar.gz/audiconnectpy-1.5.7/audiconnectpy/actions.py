"""Audi actions."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Literal

from .auth import Auth
from .const import (
    BRAND,
    FAILED,
    MAX_RESPONSE_ATTEMPTS,
    REQUEST_FAILED,
    REQUEST_STATUS_SLEEP,
    REQUEST_SUCCESSFUL,
    SUCCEEDED,
)
from .exceptions import HttpRequestError, TimeoutExceededError
from .helpers import ExtendedDict, spin_hash


@dataclass
class AudiActions:
    """Actions on vehicle."""

    auth: Auth
    vin: str
    url: str
    url_setter: str
    country: str
    api_level: dict[str, int]
    spin: str | None

    async def async_set_lock(self, lock: bool) -> None:
        """Set lock."""
        security_token = await self._async_get_security_token(
            "rlu_v1/operations/" + ("LOCK" if lock else "UNLOCK")
        )
        headers = await self.auth.async_get_action_headers(
            "application/vnd.vwg.mbb.RemoteLockUnlock_v1_0_0+xml",
            security_token,
        )
        data: str | dict[str, Any] = (
            '<?xml version="1.0" encoding= "UTF-8" ?>'
            + f'<rluAction xmlns="http://audi.de/connect/rlu"><action>{"lock" if lock else "unlock"}</action></rluAction>'
        )

        rsp = await self.auth.post(
            f"{self.url}/bs/rlu/v1/{BRAND}/{self.country}/vehicles/{self.vin}/actions",
            headers=headers,
            data=data,
            use_json=False,
        )
        rsp = rsp if rsp else ExtendedDict()
        request_id = rsp.getr("rluActionResponse.requestId")
        await self._async_check_request(
            f"{self.url}/bs/rlu/v1/{BRAND}/{self.country}/vehicles/{self.vin}/requests/{request_id}/status",
            "lock vehicle" if lock else "unlock vehicle",
            REQUEST_SUCCESSFUL,
            REQUEST_FAILED,
            "requestStatusResponse.status",
        )

    async def async_set_climater(
        self,
        start: bool,
        heater_source: Literal["electric", "auxiliary", "automatic"] = "electric",
    ) -> None:
        """Set Climatisation."""
        security_token = await self._async_get_security_token(
            "rclima_v1/operations/"
            + (
                "P_START_CLIMA_EL"
                if heater_source == "electric"
                else "P_START_CLIMA_AU"
            )
        )
        if self.api_level["climatisation"] == 3:
            # standard format with header source, e.g. E-Tron
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.ClimaterAction_v1_0_0+xml;charset=utf-8",
                security_token,
                heater_source != "electric",
            )
            data: str | dict[str, Any] = (
                f'<?xml version="1.0" encoding="UTF-8"?><action><type>{"startClimatisation" if start else "stopClimatisation"}</type><settings><heaterSource>'
                + heater_source
                + "</heaterSource></settings></action>"
            )
            use_json = False
        else:
            headers = await self.auth.async_get_action_headers(
                "application/json",
                security_token,
                heater_source != "electric",
            )
            data = (
                {
                    "action": {
                        "type": "startClimatisation",
                        "settings": {
                            "targetTemperature": 2940,
                            "climatisationWithoutHVpower": True,
                            "heaterSource": heater_source,
                            "climaterElementSettings": {
                                "isClimatisationAtUnlock": False,
                                "isMirrorHeatingEnabled": True,
                            },
                        },
                    }
                }
                if start
                else {"action": {"type": "stopClimatisation"}}
            )
            use_json = True

        rsp = await self.auth.post(
            f"{self.url}/bs/climatisation/v1/{BRAND}/{self.country}/vehicles/{self.vin}/climater/actions",
            headers=headers,
            data=data,
            use_json=use_json,
        )
        rsp = rsp if rsp else ExtendedDict()
        actionid = rsp.getr("action.actionId")
        await self._async_check_request(
            f"{self.url}/bs/climatisation/v1/{BRAND}/{self.country}/vehicles/{self.vin}/climater/actions/{actionid}",
            "start climatisation" if start else "stop climatisation",
            SUCCEEDED,
            FAILED,
            "action.actionState",
        )

    async def async_set_climater_temp(
        self,
        temperature: float = 19.5,
        heater_source: Literal["electric", "auxiliary", "automatic"] = "electric",
        glass_heating: bool = True,
        seat_fl: bool = False,
        seat_fr: bool = False,
        seat_rl: bool = False,
        seat_rr: bool = False,
    ) -> None:
        """Set Climatisation temperature."""

        # Default Temp
        temperature = int(round(temperature, 1) * 10 + 2731)

        # Construct Zone Settings
        zone_settings = [
            {"value": {"isEnabled": seat_fl, "position": "frontLeft"}},
            {"value": {"isEnabled": seat_fr, "position": "frontRight"}},
            {"value": {"isEnabled": seat_rl, "position": "rearLeft"}},
            {"value": {"isEnabled": seat_rr, "position": "rearRight"}},
        ]

        if self.api_level["climatisation"] == 3:
            # standard format with header source, e.g. E-Tron
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.ClimaterAction_v1_0_0+xml;charset=utf-8", None
            )
            data: str | dict[str, Any] = (
                '<?xml version="1.0" encoding="UTF-8"?><action><type>setSettings</type><settings>'
                + f"<targetTemperature>{temperature}</targetTemperature>"
                + "<climatisationWithoutHVpower>false</climatisationWithoutHVpower>"
                + f"<heaterSource>{heater_source}</heaterSource>"
                + "</settings></action>"
            )
            use_json = False
        else:
            headers = await self.auth.async_get_action_headers("application/json", None)
            data = {
                "action": {
                    "type": "setSettings",
                    "settings": {
                        "targetTemperature": temperature,
                        "climatisationWithoutHVpower": True,
                        "heaterSource": heater_source,
                        "climaterElementSettings": {
                            "isClimatisationAtUnlock": False,
                            "isMirrorHeatingEnabled": glass_heating,
                            "zoneSettings": {"zoneSetting": zone_settings},
                        },
                    },
                }
            }
            use_json = True
        rsp = await self.auth.post(
            f"{self.url}/bs/climatisation/v1/{BRAND}/{self.country}/vehicles/{self.vin}/climater/actions",
            headers=headers,
            data=data,
            use_json=use_json,
        )
        rsp = rsp if rsp else ExtendedDict()
        actionid = rsp.getr("action.actionId")
        await self._async_check_request(
            f"{self.url}/bs/climatisation/v1/{BRAND}/{self.country}/vehicles/{self.vin}/climater/actions/{actionid}",
            "set target temperature",
            SUCCEEDED,
            FAILED,
            "action.actionState",
        )

    async def async_set_pre_heating(self, start: bool, duration: int = 60) -> None:
        """Set pre heater."""
        security_token = await self._async_get_security_token(
            "rheating_v1/operations/" + ("P_QSACT" if start else "P_QSTOPACT")
        )
        if self.api_level["ventilation"] == 1:
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.RemoteStandheizung_v2_0_0+xml", security_token
            )
            data: str | dict[str, Any] = (
                '<?xml version="1.0" encoding= "UTF-8" ?><performAction xmlns="http://audi.de/connect/rs">'
                + f'<quickstart><active>{"true" if start else "false"}</active></quickstart></performAction>'
            )
            use_json = False
        else:
            headers = await self.auth.async_get_action_headers(
                "application/json", security_token
            )
            data = (
                {
                    "performAction": {
                        "quickstart": {
                            "startMode": "heating",
                            "active": True,
                            "climatisationDuration": duration,
                        }
                    }
                }
                if start
                else {"performAction": {"quickstop": {"active": False}}}
            )
            use_json = True

        await self.auth.post(
            f"{self.url}/bs/rs/v1/{BRAND}/{self.country}/vehicles/{self.vin}/action",
            headers=headers,
            data=data,
            use_json=use_json,
        )

    async def async_set_ventilation(self, start: bool, duration: int = 60) -> None:
        """Set ventilation."""
        security_token = await self._async_get_security_token(
            "rheating_v1/operations/" + ("P_QSACT" if start else "P_QSTOPACT")
        )
        if self.api_level["ventilation"] == 1:
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.RemoteStandheizung_v2_0_0+xml", security_token
            )
            content = (
                (
                    "<active>true</active>"
                    + f"<climatisationDuration>{duration}</climatisationDuration>"
                    + "<startMode>ventilation</startMode>"
                )
                if start
                else "<active>false</active>"
            )
            data: str | dict[str, Any] = (
                '<?xml version="1.0" encoding="UTF-8" ?><performAction xmlns="http://audi.de/connect/rs">'
                f"<quickstart>{content}</quickstart></performAction>"
            )
            use_json = False
        else:
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.RemoteStandheizung_v2_0_2+json", security_token
            )
            data = (
                {
                    "performAction": {
                        "quickstart": {
                            "startMode": "ventilation",
                            "active": True,
                            "climatisationDuration": duration,
                        }
                    }
                }
                if start
                else {"performAction": {"quickstop": {"active": False}}}
            )
            use_json = True

        await self.auth.post(
            f"{self.url}/bs/rs/v1/{BRAND}/{self.country}/vehicles/{self.vin}/action",
            headers=headers,
            data=data,
            use_json=use_json,
        )

    async def async_set_battery_charger(self, start: bool, timer: bool = False) -> None:
        """Set battery charger."""
        if self.api_level["charger"] == 2:
            headers = await self.auth.async_get_action_headers("application/json", None)
            if start and timer:
                data: str | dict[str, Any] = {
                    "action": {
                        "type": "selectChargingMode",
                        "settings": {
                            "chargeModeSelection": {"value": "timerBasedCharging"},
                        },
                    }
                }
            elif start:
                data = {"action": {"type": "start"}}
            else:
                data = {"action": {"type": "stop"}}
            use_json = True
        elif self.api_level["charger"] == 3:
            headers = await self.auth.async_get_action_headers("application/json", None)
            data = {
                "action": {
                    "type": "startBatteryCharging" if start else "stopBatteryCharging"
                }
            }
            use_json = True
        else:
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.ChargerAction_v1_0_0+xml", None
            )
            data = f'<?xml version="1.0" encoding="UTF-8" ?><action><type>{"start" if start else "stop"}</type></action>'
            use_json = False

        rsp = await self.auth.post(
            f"{self.url}/bs/batterycharge/v1/{BRAND}/{self.country}/vehicles/{self.vin}/charger/actions",
            headers=headers,
            data=data,
            use_json=use_json,
        )
        rsp = rsp if rsp else ExtendedDict()
        actionid = rsp.getr("action.actionId")
        await self._async_check_request(
            f"{self.url}/bs/batterycharge/v1/{BRAND}/{self.country}/vehicles/{self.vin}/charger/actions/{actionid}",
            "start charger" if start else "stop charger",
            SUCCEEDED,
            FAILED,
            "action.actionState",
        )

    async def async_set_charger_max(self, current: float = 32) -> None:
        """Set max current."""
        if self.api_level["charger"] == 2:
            headers = await self.auth.async_get_action_headers("application/json", None)
            data: str | dict[str, Any] = {
                "action": {
                    "settings": {"maxChargeCurrent": int(current)},
                    "type": "setSettings",
                }
            }
            use_json = True
        else:
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.ChargerAction_v1_0_0+xml", None
            )
            data = (
                '<?xml version="1.0" encoding="UTF-8" ?><action><type>setSettings</type>'
                + f"<settings><maxChargeCurrent>{current}</maxChargeCurrent></settings></action>"
            )
            use_json = False

        rsp = await self.auth.post(
            f"{self.url}/bs/batterycharge/v1/{BRAND}/{self.country}/vehicles/{self.vin}/charger/actions",
            headers=headers,
            data=data,
            use_json=use_json,
        )
        rsp = rsp if rsp else ExtendedDict()
        actionid = rsp.getr("action.actionId")
        await self._async_check_request(
            f"{self.url}/bs/batterycharge/v1/{BRAND}/{self.country}/vehicles/{self.vin}/charger/actions/{actionid}",
            "set charger max current",
            SUCCEEDED,
            FAILED,
            "action.actionState",
        )

    async def async_set_window_heating(self, start: bool) -> None:
        """Set window heating."""
        if self.api_level["windows_heating"] == 2:
            headers = await self.auth.async_get_action_headers("application/json", None)
            data: str | dict[str, Any] = {
                "action": {
                    "type": "startWindowHeating" if start else "stopWindowHeating"
                }
            }
            use_json = True
        else:
            headers = await self.auth.async_get_action_headers(
                "application/vnd.vwg.mbb.ClimaterAction_v1_0_0+xml", None
            )
            data = (
                '<?xml version="1.0" encoding= "UTF-8" ?>'
                + f"<action><type>{'startWindowHeating' if start else 'stopWindowHeating'}</type></action>"
            )
            use_json = False
        rsp = await self.auth.post(
            f"{self.url}/bs/climatisation/v1/{BRAND}/{self.country}/vehicles/{self.vin}/climater/actions",
            headers=headers,
            data=data,
            use_json=use_json,
        )
        rsp = rsp if rsp else ExtendedDict()
        actionid = rsp.getr("action.actionId")
        await self._async_check_request(
            f"{self.url}/bs/climatisation/v1/{BRAND}/{self.country}/vehicles/{self.vin}/climater/actions/{actionid}",
            "start window heating" if start else "stop window heating",
            SUCCEEDED,
            FAILED,
            "action.actionState",
        )

    async def async_set_honkflash(
        self, mode: Literal["honk", "flash"], duration: int = 15
    ) -> None:
        """Set honk and flash light."""
        rsp_position = await self.auth.get(
            f"{self.url}/bs/cf/v1/{BRAND}/{self.country}/vehicles/{self.vin}/position"
        )
        rsp_position = rsp_position if rsp_position else ExtendedDict()
        position = rsp_position.getr("findCarResponse.Position.carCoordinate")
        headers = await self.auth.async_get_action_headers("application/json", None)
        data: str | dict[str, Any] = {
            "honkAndFlashRequest": {
                "serviceOperationCode": "HONK_AND_FLASH"
                if mode == "honk"
                else "FLASH_ONLY",
                "serviceDuration": duration,
                "userPosition": {
                    "latitude": position["latitude"],
                    "longitude": position["longitude"],
                },
            }
        }
        await self.auth.post(
            f"{self.url}/bs/rhf/v1/{BRAND}/{self.country}/vehicles/{self.vin}/honkAndFlash",
            headers=headers,
            data=data,
        )

    async def async_refresh_vehicle_data(self) -> None:
        """Refresh vehicle data."""
        headers = await self.auth.async_get_headers(token_type="idk")
        region = "emea" if self.country.upper() != "US" else "na"
        data = await self.auth.post(
            f"https://{region}.bff.cariad.digital/vehicle/v1/vehicles/{self.vin}/vehiclewakeup",
            headers=headers,
        )
        data = data if data else ExtendedDict()
        request_id: str = data.getr("data.requestID")
        await self._async_pending_request(
            f"https://{region}.bff.cariad.digital/vehicle/v1/vehicles/{self.vin}/pendingrequests",
            "refresh vehicle data",
            "successful",
            "failed",
            request_id,
        )

    async def _async_check_request(
        self, url: str, action: str, success: str, failed: str, path: str
    ) -> None:
        """Check request succeeded."""
        stauts_good = False
        for _ in range(MAX_RESPONSE_ATTEMPTS):
            await asyncio.sleep(REQUEST_STATUS_SLEEP)

            rsp = await self.auth.get(url)

            status = rsp.getr(path)

            if status is None or (failed is not None and status == failed):
                raise HttpRequestError(("Cannot %s, return code '%s'", action, status))

            if status == success:
                stauts_good = True
                break

        if stauts_good is False:
            raise TimeoutExceededError(("Cannot %s, operation timed out", action))

    async def _async_pending_request(
        self, url: str, action: str, success: str, failed: str, request_id: str
    ) -> None:
        """Check request succeeded."""
        stauts_good = False
        headers = await self.auth.async_get_headers(token_type="idk")

        for _ in range(MAX_RESPONSE_ATTEMPTS):
            await asyncio.sleep(REQUEST_STATUS_SLEEP)
            rsp = await self.auth.get(url, headers=headers)
            status = None
            if rsp and (data := rsp.get("data")):
                for item in data:
                    if item.get("id") == request_id:
                        status = item.get("status")
                        break

            if status is None or (failed is not None and status == failed):
                raise HttpRequestError(("Cannot %s, return code '%s'", action, status))

            if status == success:
                stauts_good = True
                break

        if stauts_good is False:
            raise TimeoutExceededError(("Cannot %s, operation timed out", action))

    async def _async_get_security_token(self, action: str) -> Any:
        """Get security token."""
        self.spin = "" if self.spin is None else self.spin

        # Challenge
        headers = await self.auth.async_get_headers(token_type="mbb", okhttp=True)
        rsp = await self.auth.get(
            f"{self.url_setter}/rolesrights/authorization/v2/vehicles/{self.vin}/services/{action}/security-pin-auth-requested",
            headers=headers,
        )
        rsp = rsp if rsp else ExtendedDict()
        sec_token = rsp.getr("securityPinAuthInfo.securityToken")
        challenge: str = rsp.getr(
            "securityPinAuthInfo.securityPinTransmission.challenge"
        )

        # Response
        security_pin_hash = spin_hash(self.spin, challenge)
        data = {
            "securityPinAuthentication": {
                "securityPin": {
                    "challenge": challenge,
                    "securityPinHash": security_pin_hash,
                },
                "securityToken": sec_token,
            }
        }

        headers["Content-Type"] = "application/json"
        body = await self.auth.post(
            f"{self.url_setter}/rolesrights/authorization/v2/security-pin-auth-completed",
            headers=headers,
            data=data,
        )
        return body["securityToken"]
