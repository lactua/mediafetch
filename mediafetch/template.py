def template(metadata, position, status):
    inactive = '—'
    active = '\uf111'
    bar_length = 20
    length = int(int(metadata.get('length')) / 10**6)
    play = '\uf04b'
    pause = '\uf04c'

    status_icon = {'Playing': play, 'Paused': pause}[status]

    index = int(position/length*bar_length)

    time_bar = status_icon + ' ' + inactive * index + active + (bar_length - index) * inactive

    return f"""
——>  {metadata.get('title', '')}  <——

{time_bar}

Artist : {metadata.get('artist', '')}
Album : {metadata.get('album', '')}"""