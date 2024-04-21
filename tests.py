from project import HTMLSongParser


def test_parse_header():
    parser = HTMLSongParser()
    parser.feed(
        r"""
<br/><span class="SectionHeader">Verse 1</span><br/>
        """
    )
    assert len(parser.sections) == 1
    assert parser.sections == {0: 'Verse 1'}


def test_parse_chords():
    parser = HTMLSongParser()
    parser.feed(
        r"""
<table class="Lyrics"><tr>
<td class="Lyrics"><span class="ChordName">[<span class="ToolTipR">D<span class="ToolTipTextR" style="text-align: left;">Major Chord (U,M3,P5)<br />on the Perfect Unison</span></span>]</span> She&nbsp;showed&nbsp;me&nbsp;her&nbsp;room,&nbsp;isn't&nbsp;it&nbsp;good,</td>
        """
    )
    assert len(parser.lyrics) == 1
    assert parser.lyrics[0]['data'] == 'D'


def test_not_parse_invalid():
    parser = HTMLSongParser()
    parser.feed(
        r"""
        <td>D</td>
        <td>A</td>
        <td>A</td>
        """
    )
    assert len(parser.lyrics) == 0


def test_parse_lytics():
    parser = HTMLSongParser()
    parser.feed(
        r"""
        <td class="Lyrics">Never</td>
        <td class="Lyrics">Gonna</td>
        <td class="Lyrics">Give</td>
        <td class="Lyrics">You</td>
        <td class="Lyrics">Up</td>
        """
    )
    assert len(parser.lyrics) == 5
    assert parser.print().strip() == "Never Gonna Give You Up"
