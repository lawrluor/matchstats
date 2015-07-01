#parse_challonge substring parsing methods (mostly obsolete)

# given list of bottom_half items, parse lines to get relevant data for round, tag, seed, and score
def parse_bottom_match(tag_list):
  for tag in tag_list:
    match_round = str(tag.find_all("div", {"class" : "inner_content"}))
    span_tag = str(tag.find("span")) 
    div_seed = str(tag.find_all("div", {"class" : "bottom_seed"}))
    div_score = str(tag.find_all("div", {"class" : "bottom_score"}))

    # dictionary containing relevant data to be returned
    bottom_half  = {}
    
    if match_round and len(match_round) > 2:
      start_text = "data-round=\""
      end_text = "\"><"

      start_index = match_round.find(start_text) + 12
      end_index = match_round.find(end_text)
      bottom_half["round"] = match_round[start_index:end_index]

    if span_tag and len(span_tag) > 0:
      processed_span_tag = '~' + span_tag[1:]
      start_index = processed_span_tag.index('>') + 1
      end_index = processed_span_tag.index('<')
      bottom_half["tag"] = span_tag[start_index:end_index]
    
    if div_seed and len(div_seed) > 2:
      processed_div_seed = '~' + div_seed[2:]
      start_index = processed_div_seed.index('>') + 1
      end_index = processed_div_seed.index('<')
      bottom_half["seed"] = processed_div_seed[start_index:end_index]

    if div_score and len(div_score) > 2:
      processed_div_score = '~' + div_score[2:] 
      start_index = processed_div_score.index('>') + 1
      end_index = processed_div_score.index('<') 
      # Check for alternate win scores: checkmark Unicode character, empty score
      if processed_div_score[start_index:end_index] == "\xe2\x9c\x93":
        bottom_half["score"] = 1
      elif processed_div_score[start_index:end_index] == '':
        bottom_half["score"] = 0
      else:
        bottom_half["score"] = 0

    return bottom_half