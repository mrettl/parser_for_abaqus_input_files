import unittest

from abq import inp


class AbaqusInputTestCase(unittest.TestCase):
    def test_read_write(self):
        inp_content = inp.read_from_file("../../res/inp/test/2D_jintegral2d_cpe8.inp")
        self.assertEqual(34, len(inp_content))
        self.assertEqual(inp_content[0], "**Comment 1")
        self.assertEqual(inp_content[-8], dict(
            keyword="*CONTOUR INTEGRAL",
            parameters=dict(
                FREQUENCY=1,
                CONTOURS=3,
                SYMM=None,
                OUTPUT="BOTH",
                TYPE="T-STRESS"
            ),
            data=[
                ["CRACK", -1., 0.]
            ]
        ))

        # write/read from string
        file_content = inp.write_to_string(inp_content)
        inp_content_reload = inp.read_from_string(file_content)
        self.assertEqual(inp_content, inp_content_reload)

        # write/read from file
        inp.write_to_file("../../res/inp/test/2D_jintegral2d_cpe8_out.inp", inp_content)
        inp_content_reload = inp.read_from_file("../../res/inp/test/2D_jintegral2d_cpe8_out.inp")
        self.assertEqual(inp_content, inp_content_reload)

        # count lines
        with open("../../res/inp/test/2D_jintegral2d_cpe8.inp", "r") as inp_file:
            expected_line_number = len(inp_file.readlines())

        with open("../../res/inp/test/2D_jintegral2d_cpe8_out.inp", "r") as inp_file:
            actual_line_number = len(inp_file.readlines())

        self.assertEqual(expected_line_number, actual_line_number)

if __name__ == '__main__':
    unittest.main()
