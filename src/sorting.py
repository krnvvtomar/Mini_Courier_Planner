"""Parcel prioritization using a stable sorting strategy."""
from datetime import datetime

def sort_parcels(parcels):
    """
    Sort by earliest deadline first, then higher priority, then parcel ID.
    Priority labels are HIGH, MEDIUM, LOW.
    """
    priority_rank = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    def key(parcel):
        deadline = datetime.strptime(parcel["deadline"], "%H:%M")
        return (deadline, -priority_rank[parcel["priority"].upper()], parcel["parcel_id"])
    return sorted(parcels, key=key)
