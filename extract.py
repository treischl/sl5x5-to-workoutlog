from openpyxl import load_workbook
import re

p = re.compile(r'(\d+)\D(\d+\.?\d*)')

class Extract():
    @staticmethod
    def getoldworkouts(filename):
        oldworkouts = dict()

        wb = load_workbook(filename, read_only=True)
        ws = wb.worksheets[0]
        for row in ws.rows:
            movement = dict()
            movement['date'] = row[0].value.isoformat().split('T')[0]
            movement['name'] = row[1].value
            movement['reps'] = [[int(m.group(1)), float(m.group(2))] \
                                for m in [p.match(r.value) \
                                            for r in row[2:] \
                                            if r.value]]

            if (movement['date'] not in oldworkouts):
                oldworkouts[movement['date']] = [movement]
            else:
                oldworkouts[movement['date']].append(movement)

        return oldworkouts
