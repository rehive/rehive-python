def flatten_files(entries):
    """
    Flatten a list of `{file, label?, description?}` dicts into the bracketed
    multipart keys (`files[<i>][file]`, `files[<i>][label]`,
    `files[<i>][description]`) accepted by the document create endpoints.

    A `None` entry skips that index, which is how an optional position in
    `DocumentType.file_rules` is left unfilled while still aligning later
    entries to their rule indices.
    """

    out = {}
    for i, entry in enumerate(entries):
        if entry is None:
            continue
        if not isinstance(entry, dict):
            raise TypeError(
                "files[{}] must be a dict or None.".format(i)
            )
        file_obj = entry.get('file')
        if file_obj is None:
            raise ValueError(
                "files[{}] is missing a 'file' entry.".format(i)
            )
        out['files[{}][file]'.format(i)] = file_obj
        for key in ('label', 'description'):
            value = entry.get(key)
            if value is not None:
                out['files[{}][{}]'.format(i, key)] = value
    return out
