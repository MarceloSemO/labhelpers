def init_file(outfile, headers):
    if outfile is None:
        return None
    f = open(outfile, 'w+', buffering=1)
    f.write("{}\n".format(', '.join(headers)))
    return f
