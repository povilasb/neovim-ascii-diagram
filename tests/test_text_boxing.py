from hamcrest import assert_that, is_, starts_with

from ascii_diagram import box_area, Coords, horizontal_border, \
    with_vertical_borders


def describe_box_area():
    def describe_when_single_line_is_selected():
        def describe_when_all_columns_selected():
            def it_is_decorated_with_borders():
                boxed = box_area(['hello'], Coords(0, 0), Coords(4, 0))

                assert_that(boxed, is_([
                    '+-------+',
                    '| hello |',
                    '+-------+',
                ]))

        def describe_when_selected_columns_are_surrounded_by_other_characters():
            def it_wraps_only_those_columns():
                boxed = box_area(['hello'], Coords(1, 0), Coords(3, 0))

                assert_that(boxed, is_([
                    ' +-----+',
                    'h| ell |o',
                    ' +-----+',
                ]))

    def describe_when_multiple_lines_are_selected():
        def describe_when_all_columns_selected():
            def it_is_decorated_with_borders():
                boxed = box_area(['hello', 'world'], Coords(0, 0), Coords(4, 1))

                assert_that(boxed, is_([
                    '+-------+',
                    '| hello |',
                    '| world |',
                    '+-------+',
                ]))


def describe_horizontal_border():
    def describe_when_x1_is_greater_than_0():
        def it_adds_spaces_margin():
            border = horizontal_border(2, 4)

            assert_that(border, starts_with('  '))

    def it_pads_border_by_spaces():
        border = horizontal_border(3, 5)

        assert_that(border, is_('   +-----+'))


def describe_with_vertical_borders():
    def it_wraps_string_with_vertical_bars():
        boxed = with_vertical_borders('..hello..', 2, 6)

        assert_that(boxed, is_('..| hello |..'))
