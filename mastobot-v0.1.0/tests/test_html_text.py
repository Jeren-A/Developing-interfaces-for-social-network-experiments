from ..mastobot.utils import normalize_content


def test_html_text():
    assert (
        normalize_content(
            '<p><span class="h-card"><a href="https://yeet.social/@c18n" '
            'class="u-url mention">@<span>c18n</span></a></span> text '
            '<a href="https://mastodon.technology/tags/tag" '
            'class="mention hashtag" rel="tag">#<span>tag</span></a> '
            ":cate: ®️ @ someone # sometag</p>"
        )
        == "@c18n text #tag :cate: ®️ @ someone # sometag"
    )

    assert normalize_content(
        "<p>Take a look at the "
        '<a href="https://mastodon.technology/tags/Akademy2020" '
        'class="mention hashtag" rel="tag">'
        "#<span>Akademy2020</span></a>"
        "program and mark your calendars for all of the great talks we have in store! "
        '<a href="https://akademy.kde.org/2020/program" '
        'rel="nofollow noopener noreferrer" target="_blank">'
        '<span class="invisible">https://</span>'
        '<span class="">akademy.kde.org/2020/program</span>'
        '<span class="invisible"></span></a>  <br />Don’t forget to register too! '
        '<a href="https://akademy.kde.org/2020/register" '
        'rel="nofollow noopener noreferrer" target="_blank">'
        '<span class="invisible">https://</span>'
        '<span class="">akademy.kde.org/2020/register</span>'
        '<span class="invisible"></span></a></p>'
    ) == (
        "Take a look at the #Akademy2020 program and mark your calendars "
        "for all of the great talks we have in store! "
        "https://akademy.kde.org/2020/program\n"
        "Don’t forget to register too! https://akademy.kde.org/2020/register"
    )


if __name__ == "__main__":
    test_html_text()
