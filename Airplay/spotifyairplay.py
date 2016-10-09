import sys
import json
import fileinput
import urllib2
import re
import pdb
sys.path.append( "../Modules")
import spotify_methods as sptfy


def main(ultimatechart, explicit = False):

    cleans = []
    explicits = []
    local_tracks = []

    cleans, local_tracks = sptfy.pullSpotifyTracks('../input/cleans.txt')
    explicits, local_tracks = sptfy.pullSpotifyTracks(
          '../input/explicits.txt'
        , tracks = explicits
        , local_tracks = local_tracks
    )

    if explicit:
        # sort explicit list
        sorted_tracks = sorted(explicits, key=lambda x: float(x['popularity']), reverse=True)
    else:
        # sort explicit list
        sorted_tracks = sorted(explicits, key=lambda x: float(x['popularity']), reverse=True)
        # now replace explicits with cleans
        for e in explicits: # replace explicit track href by the clean version's href
            for c in cleans:
                if e['artist'] in c['artist'] and e['title'][:3] in c['title'][:3]: # compare artist name and first 4 characters of track name
                    e['spotify_id'] = c['spotify_id']

    print "\n"
    for item in sorted_tracks:
        print str(item['popularity']) + " :: " + item['artist'] + " - " + item['title']
    print "\n"
    for item in sorted_tracks:
        print "spotify:track:{}".format(item['spotify_id'].strip())
    for item in local_tracks:
        print item
    print "\n"

    if ultimatechart is not None:
        print "Look in to keeping the following songs in Airplay this week...\n"
        for item in sorted_tracks:
            if item['popularity'] < 75:
                artist = item['artist']
                title = item['title']
                artist = re.sub(r'([^\s\w]|_)+', '', artist)
                title = re.sub(r'([^\s\w]|_)+', '', title)
                artist_matches = re.findall(r"(?=("+'|'.join(artist.split())+r"))", ultimatechart)
                title_matches = re.findall(r"(?=("+'|'.join(title.split())+r"))", ultimatechart)
                if len(artist_matches) and len(title_matches):
                    print str(item['popularity']) + " :: " + item['artist'] + " - " + item['title']
    else:
        print "If you want to compare to Ultimate Chart, please provide a txt version as an arg."


if __name__ == "__main__":
    explicit = False
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            ultimatechart = f.read()
        if len(sys.argv) == 3 and sys.argv[2] == 'explicit':
            explicit = True
    else:
        ultimatechart = None
        print "If you want to compare to Ultimate Chart, please provide a txt version as an arg."

    main(ultimatechart, explicit)
