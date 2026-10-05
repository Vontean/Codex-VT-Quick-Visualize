import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / 'skill' / 'quick-visualize'
sys.path.insert(0, str(SKILL / 'scripts'))
from render import render_checked


class ChartContractTests(unittest.TestCase):
    def render_spec(self, kind, spec):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'spec.json'
            output = Path(directory) / 'chart.html'
            source.write_text(json.dumps(spec))
            result = render_checked(kind, source, output)
            return result, output.read_text() if output.exists() else ''

    def test_four_bar_series_and_variable_categories(self):
        spec = {'title': 'Four', 'x_axis_label': 'Group', 'y_axis_label': 'Value',
                'categories': ['A', 'B'], 'series': [
                    {'name': str(i), 'values': [0, i]} for i in range(4)]}
        result, _ = self.render_spec('grouped-bar-chart', spec)
        self.assertTrue(result['ok'], result)
        spec['series'].append({'name': 'fifth', 'values': [0, 1]})
        result, _ = self.render_spec('grouped-bar-chart', spec)
        self.assertFalse(result['ok'])
        self.assertEqual(result['stage'], 'render')

    def test_line_minimum_and_maximum_dates(self):
        from datetime import date, timedelta
        for count in [2, 90]:
            with self.subTest(count=count):
                spec = {'title': 'Values', 'x_axis_label': 'Date', 'y_axis_label': 'Cost',
                        'decimals': 2, 'value_prefix': '$', 'value_suffix': 'k',
                        'points': [{'date': str(date(2025, 1, 1) + timedelta(days=i)),
                                    'value': i / 10, 'description': 'details'} for i in range(count)]}
                result, fragment = self.render_spec('line-chart', spec)
                self.assertTrue(result['ok'], result)
                self.assertIn('"decimals":2', fragment)
                self.assertIn('"description":"details"', fragment)

    def test_donut_zero_slice_and_script_escaping(self):
        spec = {'title': '</script><img>', 'items': [
            {'label': '</script><img>', 'value': 0, 'description': 'literal'},
            {'label': 'Rest', 'value': 10}]}
        result, fragment = self.render_spec('donut-chart', spec)
        self.assertTrue(result['ok'], result)
        self.assertNotIn('</script><img>', fragment)
        self.assertIn('\\u003c/script\\u003e', fragment)
        spec['items'][1]['value'] = 0
        result, _ = self.render_spec('donut-chart', spec)
        self.assertFalse(result['ok'])

    def test_radar_dimension_extremes(self):
        for dimensions, objects in [(3, 1), (8, 4)]:
            with self.subTest(dimensions=dimensions, objects=objects):
                spec = {'title': 'Profiles', 'max_value': 10,
                        'dimensions': [str(i) for i in range(dimensions)],
                        'series': [{'name': str(i), 'values': [i] * dimensions} for i in range(objects)]}
                result, _ = self.render_spec('radar-chart', spec)
                self.assertTrue(result['ok'], result)


if __name__ == '__main__':
    unittest.main()
