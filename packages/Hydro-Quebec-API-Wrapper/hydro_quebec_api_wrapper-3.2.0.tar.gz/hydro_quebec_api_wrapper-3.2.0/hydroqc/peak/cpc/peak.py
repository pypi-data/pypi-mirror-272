"""Class describing a period."""

import datetime

from hydroqc.error import HydroQcCPCPeakError
from hydroqc.peak.cpc.consts import (
    DEFAULT_ANCHOR_DURATION,
    DEFAULT_ANCHOR_START_OFFSET,
    DEFAULT_EVENING_PEAK_END,
    DEFAULT_EVENING_PEAK_START,
    DEFAULT_MORNING_PEAK_END,
    DEFAULT_MORNING_PEAK_START,
    DEFAULT_PRE_HEAT_DURATION,
    MORNING_EVENING,
)
from hydroqc.timerange import TimeRange
from hydroqc.types import CriticalPeakDataTyping
from hydroqc.utils import EST_TIMEZONE

__all__ = ["Anchor", "PreHeat", "Peak"]


class Anchor(TimeRange):
    """This class describe a period object."""

    def __init__(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        is_critical: bool = False,
    ):
        """Period constructor."""
        super().__init__(start_date, end_date, is_critical)


class PreHeat(TimeRange):
    """This class describe a period object."""

    def __init__(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        is_critical: bool = False,
    ):
        """Period constructor."""
        super().__init__(start_date, end_date, is_critical)


class Peak(TimeRange):
    """This class describe a period object."""

    # preheat: PreHeat
    # anchor: Anchor
    # _is_critical: bool

    def __init__(
        self,
        date: datetime.datetime,
        # TODO: use enum
        morning_evening: str,
        preheat_duration: int = DEFAULT_PRE_HEAT_DURATION,
    ):
        """Period constructor."""
        if morning_evening not in MORNING_EVENING:
            msg = f"Peak type {morning_evening} needs be one of {MORNING_EVENING}"
            raise HydroQcCPCPeakError(msg)
        self._morning_evening: str = morning_evening
        self._date: datetime.datetime = date.astimezone(EST_TIMEZONE)
        self._preheat_duration: int = preheat_duration
        super().__init__(self.start_date, self.end_date, is_critical=False)
        self._raw_stats: CriticalPeakDataTyping = {}

    @property
    def is_morning(self) -> bool:
        """Return True if it's a morning peak."""
        return self._morning_evening == "morning"

    @property
    def is_evening(self) -> bool:
        """Return True if it's a evening peak."""
        return self.morning_evening == "evening"

    @property
    def morning_evening(self) -> str:
        """Return evening or morning peak value."""
        return self._morning_evening

    @property
    def is_critical(self) -> bool:
        """Return True peak is critical."""
        return self._is_critical

    def set_critical(self, stats: CriticalPeakDataTyping) -> None:
        """Save critical stats in the peak and set it as critical."""
        self._is_critical = True
        self._raw_stats = stats

    @property
    def day(self) -> datetime.date:
        """Get the day, without time, of the peak."""
        return self._date.date()

    @property
    def anchor(self) -> Anchor:
        """Get the anchor period of the peak."""
        anchor_start_date = self.start_date - datetime.timedelta(
            hours=DEFAULT_ANCHOR_START_OFFSET
        )
        anchor_end_date = anchor_start_date + datetime.timedelta(
            hours=DEFAULT_ANCHOR_DURATION
        )
        return Anchor(anchor_start_date, anchor_end_date, self.is_critical)

    @property
    def preheat(self) -> PreHeat:
        """Get the preheat period of the peak."""
        preheat_start_date = self.start_date - datetime.timedelta(
            minutes=self._preheat_duration
        )
        return PreHeat(preheat_start_date, self.start_date, self.is_critical)

    @property
    def start_date(self) -> datetime.datetime:
        """Get the start date of the peak."""
        if self._morning_evening not in ("morning", "evening"):
            msg = f"Peak type {self._morning_evening} needs be one of {MORNING_EVENING}"
            raise HydroQcCPCPeakError(msg)
        if self._morning_evening == "morning":
            start_date = self._date.replace(
                hour=DEFAULT_MORNING_PEAK_START.hour,
                minute=DEFAULT_MORNING_PEAK_START.minute,
                second=DEFAULT_MORNING_PEAK_START.second,
            )
        else:
            # evening
            start_date = self._date.replace(
                hour=DEFAULT_EVENING_PEAK_START.hour,
                minute=DEFAULT_EVENING_PEAK_START.minute,
                second=DEFAULT_EVENING_PEAK_START.second,
            )
        return start_date

    @property
    def end_date(self) -> datetime.datetime:
        """Get the end date of the peak."""
        if self._morning_evening not in ("morning", "evening"):
            msg = f"Peak type {self._morning_evening} needs be one of {MORNING_EVENING}"
            raise HydroQcCPCPeakError(msg)
        if self._morning_evening == "morning":
            end_date = self._date.replace(
                hour=DEFAULT_MORNING_PEAK_END.hour,
                minute=DEFAULT_MORNING_PEAK_END.minute,
                second=DEFAULT_MORNING_PEAK_END.second,
            )
        else:
            # evening
            end_date = self._date.replace(
                hour=DEFAULT_EVENING_PEAK_END.hour,
                minute=DEFAULT_EVENING_PEAK_END.minute,
                second=DEFAULT_EVENING_PEAK_END.second,
            )
        return end_date

    @property
    def credit(self) -> float | None:
        """Get credit save during this peak.

        Return None if the peak is not critical.
        """
        return self._raw_stats.get("montantEffacee")

    @property
    def ref_consumption(self) -> float | None:
        """Get reference consumption during this peak.

        Return None if the peak is not critical.
        """
        return self._raw_stats.get("consoReference")

    @property
    def actual_consumption(self) -> float | None:
        """Get actual consumption during this peak.

        Return None if the peak is not critical.
        """
        return self._raw_stats.get("consoReelle")

    @property
    def saved_consumption(self) -> float | None:
        """Get saved consumption during this peak.

        Return None if the peak is not critical.
        """
        return self._raw_stats.get("consoEffacee")

    @property
    def consumption_code(self) -> str | None:
        """Get code consumption during this peak.

        Return None if the peak is not critical.
        """
        return self._raw_stats.get("codeConso")

    @property
    def is_billed(self) -> bool | None:
        """Return True if the cpc was billed.

        Return None if the peak is not critical.
        """
        return self._raw_stats.get("indFacture")
