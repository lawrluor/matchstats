from operator import attrgetter

# Given setlist, sorts sets by set id
def sort_setlist(setlist):
  sorted_setlist = sorted(setlist, key=lambda set: set.id)
  return sorted_setlist


# Given list of Placement objects, order by associated Tournament.date, then Tournament.name
def sort_placementlist(placementlist):
  sorted_placementlist = sorted(placementlist, key=attrgetter('tournament.date', 'tournament.name'), reverse=True)
  return sorted_placementlist
