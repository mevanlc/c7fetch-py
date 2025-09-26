"""NegColTable - A Table subclass with negative width column support."""

import copy
from functools import wraps
from typing import TYPE_CHECKING, Any, List, Optional

from rich.console import Console, ConsoleRenderable, RichCast
from rich.table import Column, Table

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult
    from rich.measure import Measurement



class NegColTable(Table):
    """A Table subclass that supports negative width columns.

    A negative width column (negcol) has lower priority than normal columns
    and shrinks to fit available space. If it can't meet its min_width,
    the column is excluded from rendering.

    Constraints:
    - Only one negative width column allowed
    - All columns must have no_wrap=True
    """

    def _has_negcol(self) -> Optional[Column]:
        """Returns the negcol if exists, else None.

        Raises:
            ValueError: If more than one negcol exists or no_wrap constraint violated.
        """
        negcols = [col for col in self.columns if col.width and col.width < 0]

        if len(negcols) > 1:
            raise ValueError("Only one negative width column allowed")

        if negcols and not all(col.no_wrap for col in self.columns):
            raise ValueError("All columns must have no_wrap=True when using negcol")

        return negcols[0] if negcols else None

    def _negcol_fits(self, console: "Console", options: "ConsoleOptions") -> bool:
        """Check if negcol fits within available space respecting min_width.

        Args:
            console: Console instance for rendering context
            options: Console options for width constraints

        Returns:
            True if negcol fits or no negcol exists, False otherwise
        """
        negcol = self._has_negcol()
        if not negcol:
            return True

        # Calculate space used by non-negcol columns
        total_used = self._extra_width

        for col in self.columns:
            if col is not negcol:
                measurement = self._measure_column(console, options, col)
                # Use fixed width if specified, otherwise use measured maximum
                width = col.width if col.width is not None else measurement.maximum
                total_used += width

        # Determine available space for negcol
        max_width = self.width if self.width is not None else options.max_width
        available = max_width - total_used

        # Check if available space meets minimum width requirement
        min_required = negcol.min_width or 1
        return available >= min_required

    def _deepcopy_without_negcol(self) -> "NegColTable":
        """Create deep copy of table with negcol removed.

        Returns:
            New NegColTable instance without the negative width column
        """
        negcol = self._has_negcol()
        if not negcol:
            return copy.deepcopy(self)

        # Create deep copy
        temp = copy.deepcopy(self)

        # Find and remove negcol
        negcol_idx = negcol._index # pyright: ignore[reportPrivateUsage]
        del temp.columns[negcol_idx]

        # Re-index remaining columns
        for i, col in enumerate(temp.columns):
            col._index = i # pyright: ignore[reportPrivateUsage]
            # Note: Each column maintains its own _cells list,
            # so we don't need to remove cells - they go with the column

        return temp

    def _calculate_column_widths_with_negcol(self, console: "Console", options: "ConsoleOptions") -> List[int]:
        """Calculate column widths when a negcol is present.

        Args:
            console: Console instance
            options: Console options

        Returns:
            List of column widths including calculated negcol width
        """
        negcol = self._has_negcol()
        if not negcol:
            return super()._calculate_column_widths(console, options)

        # Initialize widths list
        widths = [0] * len(self.columns)
        total_used = self._extra_width

        # Calculate widths for non-negcol columns
        for col in self.columns:
            if col is negcol:
                continue

            # Measure column
            measurement = self._measure_column(console, options, col)

            # Use fixed width if specified, otherwise use measured maximum
            if col.width is not None:
                width = col.width
            else:
                width = measurement.maximum

            widths[col._index] = width # pyright: ignore[reportPrivateUsage]
            total_used += width

        # Calculate available space for negcol
        max_width = self.width if self.width is not None else options.max_width
        available = max_width - total_used

        # Assign width to negcol (caller should have already verified it fits)
        widths[negcol._index] = max(available, negcol.min_width or 1) # pyright: ignore[reportPrivateUsage]

        return widths

    def _calculate_column_widths(self, console: "Console", options: "ConsoleOptions") -> List[int]:
        """Calculate column widths, handling negcol if present.

        Args:
            console: Console instance
            options: Console options

        Returns:
            List of column widths
        """
        if self._has_negcol():
            if self._negcol_fits(console, options):
                return self._calculate_column_widths_with_negcol(console, options)
            else:
                temp = self._deepcopy_without_negcol()
                return temp._calculate_column_widths(console, options)
        else:
            return super()._calculate_column_widths(console, options)

    def __rich_console__(self, console: "Console", options: "ConsoleOptions") -> "RenderResult":
        """Render the table to the console.

        Args:
            console: Console instance
            options: Console options

        Yields:
            Rendered segments
        """
        if self._has_negcol():
            if self._negcol_fits(console, options):
                # Render normally with negcol
                yield from super().__rich_console__(console, options)
            else:
                # Render without negcol
                temp = self._deepcopy_without_negcol()
                yield from temp.__rich_console__(console, options)
        else:
            yield from super().__rich_console__(console, options)

    def __rich_measure__(self, console: "Console", options: "ConsoleOptions") -> Measurement:
        """Measure the minimum and maximum width of the table.

        Args:
            console: Console instance
            options: Console options

        Returns:
            Measurement with minimum and maximum widths
        """
        if self._has_negcol():
            if self._negcol_fits(console, options):
                # Measure with negcol included
                return super().__rich_measure__(console, options)
            else:
                # Measure without negcol
                temp = self._deepcopy_without_negcol()
                return temp.__rich_measure__(console, options)
        else:
            return super().__rich_measure__(console, options)

class NegColColumn(Column):
    @wraps(Column.__init__, assigned=['__signature__'])
    def __init__(self, *args: object, **kwargs: object):
        """A Column subclass that supports negative width.

        A negative width column (negcol) has lower priority than normal columns
        and shrinks to fit available space. If it can't meet its min_width,
        the column is excluded from rendering.

        Constraints:
        - Only one negative width column allowed per table
        - All columns must have no_wrap=True
        """
        kw_min_width = kwargs.get("min_width")
        if isinstance(kw_min_width, int) and kw_min_width < 0:
            min_width = self._min_width_from_header_len(kwargs)
            kwargs["min_width"] = min_width
        
        super().__init__(*args, **kwargs) # type: ignore[call-arg]


    def _min_width_from_header_len(self, kwargs: dict[str, Any]) -> Optional[int]:
        """Determine min_width based on header length if min_width is negative.

        Args:
            kwargs: Keyword arguments passed to constructor
        Returns:
            Calculated min_width based on header length
        """
        kw_header = kwargs.get("header")
        if kw_header is None:
            return None
        if isinstance(kw_header, str) and len(kw_header) > 0:
            kw_min_width = len(kw_header)
        elif isinstance(kw_header, RichCast):
            while isinstance(kw_header, RichCast):
                kw_header = kw_header.__rich__()
        elif not isinstance(kw_header, ConsoleRenderable):
            raise ValueError(f"Invalid header type for min_width calculation: {type(kw_header)}")
        if isinstance(kw_header, ConsoleRenderable):
            console = Console()
            kw_min_width = console.measure(kw_header).maximum
        else:
            kw_min_width = len(kw_header)
        return kw_min_width
