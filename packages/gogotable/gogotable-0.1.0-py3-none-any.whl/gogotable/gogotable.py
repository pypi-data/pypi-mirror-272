def gogotable(headers, rows):  # noqa
    """
    Go Go Table

    :param headers: headers of the table
    :param rows: the data of the table
    :return: a list of strings representing the table
    """

    table = []
    skip_data = False

    # Find the size of each column
    columns_length = []
    for i, _ in enumerate(headers):
        try:
            column_length = max(len(str(row[i])) for row in rows)
        except IndexError:
            column_length = 0
        except ValueError:
            # There are no rows to calculate the max
            column_length = 0
            skip_data = True

        # Sometimes, the header size is greater than the value
        if len(headers[i]) > column_length:
            column_length = len(headers[i])

        columns_length.append(column_length)

    header_line = (
        "|"
        + "|".join(
            f" {header:^{length}} " for header, length in zip(headers, columns_length)
        )
        + "|"
    )
    border = "|" + "-".join("-" * (length + 2) for length in columns_length) + "|"
    table.extend([border, header_line, border])

    if not skip_data:
        # Build the table data rows
        for row in rows:
            data_line = (
                "|"
                + "|".join(
                    f" {data:>{length}} " for data, length in zip(row, columns_length)
                )
                + "|"
            )
            table.append(data_line)

    table.append(border)

    return table
