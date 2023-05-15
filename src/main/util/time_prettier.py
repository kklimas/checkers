class TimePrettier:
    @staticmethod
    def prettify_millis(millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)

        millis = str(millis % 1000)
        seconds = str(seconds)
        minutes = str(minutes)

        if len(millis) == 1:
            millis = '00' + millis
        elif len(millis) == 2:
            millis = '0' + millis

        if len(seconds) == 1:
            seconds = '0' + seconds

        if len(minutes) == 1:
            minutes = '0' + minutes

        return minutes + ':' + seconds + ':' + millis
