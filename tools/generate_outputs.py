#!/usr/bin/env python3
import os
from pathlib import Path
from typing import List, Dict

from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt

OUTPUT_DIR = Path('/workspace/generated')
IMAGES_DIR = OUTPUT_DIR / 'images'


def ensure_dirs() -> None:
	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def save_right_triangle_image(path: Path, leg_a: int, leg_b: int) -> None:
	fig, ax = plt.subplots(figsize=(3, 3))
	ax.plot([0, leg_a], [0, 0], 'k-', linewidth=2)
	ax.plot([0, 0], [0, leg_b], 'k-', linewidth=2)
	ax.plot([leg_a, 0], [0, leg_b], 'k--', linewidth=2)
	# Right angle box
	xb, yb, s = 0, 0, min(leg_a, leg_b) * 0.15
	ax.plot([xb, xb + s], [yb, yb], 'k-', linewidth=2)
	ax.plot([xb, xb], [yb, yb + s], 'k-', linewidth=2)
	ax.plot([xb + s, xb + s], [yb, yb + s], 'k-', linewidth=2)
	ax.plot([xb, xb + s], [yb + s, yb + s], 'k-', linewidth=2)
	ax.text(leg_a / 2, -0.5, f'{leg_a}', ha='center', va='top')
	ax.text(-0.5, leg_b / 2, f'{leg_b}', ha='right', va='center', rotation=90)
	ax.set_xlim(-1, max(leg_a, leg_b) + 1)
	ax.set_ylim(-1, max(leg_a, leg_b) + 1)
	ax.set_aspect('equal')
	ax.axis('off')
	fig.tight_layout()
	fig.savefig(path, dpi=200, bbox_inches='tight')
	plt.close(fig)


def save_fruit_barchart_image(path: Path, labels: List[str], values: List[int]) -> None:
	fig, ax = plt.subplots(figsize=(4, 3))
	bars = ax.bar(labels, values, color=['#4e79a7', '#f28e2b', '#59a14f'])
	for bar, v in zip(bars, values):
		ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, str(v), ha='center', va='bottom')
	ax.set_ylim(0, max(values) + 2)
	ax.set_ylabel('Count')
	ax.set_title('Fruit Counts')
	fig.tight_layout()
	fig.savefig(path, dpi=200, bbox_inches='tight')
	plt.close(fig)


def build_new_questions_blocks() -> List[Dict[str, str]]:
	return [
		{
			"title": "Right Triangle Hypotenuse",
			"description": "Find the hypotenuse of a right triangle using the Pythagorean theorem.",
			"question": "In the right triangle shown, the legs have lengths 6 and 8 units. What is the length of the hypotenuse?",
			"instruction": "Select the correct value of the hypotenuse.",
			"difficulty": "easy",
			"order": "1",
			"options": ["7", "8", "9", "10", "14"],
			"answer": "10",
			"explanation": "By the Pythagorean theorem, c = \\sqrt{6^{2} + 8^{2}} = \\sqrt{36 + 64} = \\sqrt{100} = 10.",
			"subject": "Quantitative Math",
			"unit": "Geometry and Measurement",
			"topic": "Right Triangles & Trigonometry",
			"image_path": str(IMAGES_DIR / 'q_new_triangle.png')
		},
		{
			"title": "Average Fruit Count",
			"description": "Compute the mean from a bar chart of three categories.",
			"question": "The bar chart shows the counts of Apples, Bananas, and Cherries collected by a class. What is the mean (average) count across the three fruits?",
			"instruction": "Choose the mean of the displayed counts.",
			"difficulty": "moderate",
			"order": "2",
			"options": ["6", "6.5", "7", "7.5", "8"],
			"answer": "7",
			"explanation": "If the counts are 4, 7, and 10, then mean = (4+7+10)/3 = 21/3 = 7.",
			"subject": "Quantitative Math",
			"unit": "Data Analysis & Probability",
			"topic": "Mean, Median, Mode, & Range",
			"image_path": str(IMAGES_DIR / 'q_new_bars.png')
		}
	]


def write_new_questions_docx(blocks: List[Dict[str, str]], path: Path) -> None:
	doc = Document()
	for b in blocks:
		doc.add_paragraph(f"@title {b['title']}")
		doc.add_paragraph(f"@description {b['description']}")
		doc.add_paragraph("")
		doc.add_paragraph(f"@question {b['question']}")
		doc.add_paragraph(f"@instruction {b['instruction']}")
		doc.add_paragraph(f"@difficulty {b['difficulty']}")
		doc.add_paragraph(f"@Order {b['order']}")
		# options with correct marked using @@option
		for opt in b['options']:
			if opt == b['answer']:
				doc.add_paragraph(f"@@option {opt}")
			else:
				doc.add_paragraph(f"@option {opt}")
		doc.add_paragraph("@explanation")
		doc.add_paragraph(b['explanation'])
		doc.add_paragraph(f"@subject {b['subject']}")
		doc.add_paragraph(f"@unit {b['unit']}")
		doc.add_paragraph(f"@topic {b['topic']}")
		doc.add_paragraph("@plusmarks 1")
		# Add image if present
		img_path = b.get('image_path')
		if img_path and Path(img_path).exists():
			doc.add_picture(img_path, width=Inches(3.5))
		doc.add_paragraph("")
		doc.add_paragraph("---")
		doc.add_paragraph("")
	doc.save(path)


def render_question_block(
	*,
	title: str,
	description: str,
	question: str,
	instruction: str,
	difficulty: str,
	order: int,
	options: List[str],
	answer: str,
	explanation: str,
	subject: str,
	unit: str,
	topic: str,
) -> str:
	lines: List[str] = []
	lines.append(f"@title {title}")
	lines.append(f"@description {description}")
	lines.append("")
	lines.append(f"@question {question}")
	lines.append(f"@instruction {instruction}")
	lines.append(f"@difficulty {difficulty}")
	lines.append(f"@Order {order}")
	for opt in options:
		prefix = '@@option' if opt == answer else '@option'
		lines.append(f"{prefix} {opt}")
	lines.append("@explanation")
	lines.append(explanation)
	lines.append(f"@subject {subject}")
	lines.append(f"@unit {unit}")
	lines.append(f"@topic {topic}")
	lines.append("@plusmarks 1")
	lines.append("")
	return "\n".join(lines)


def build_25_questions_text() -> str:
	blocks: List[str] = []
	add = blocks.append

	# 1
	add(render_question_block(
		title='Solve Linear Equation (One-Step)',
		description='Solve for n in a simple linear equation.',
		question='If $n+5=5$, what is the value of $n$?',
		instruction='Select the correct value of n.',
		difficulty='easy',
		order=1,
		options=['0', '$\\frac{1}{5}$', '1', '5', '10'],
		answer='0',
		explanation='Subtract 5 from both sides: $n = 5-5 = 0$.',
		subject='Quantitative Math', unit='Algebra', topic='Interpreting Variables'
	))

	# 2 (sequence)
	add(render_question_block(
		title='Repeating Shape Sequence',
		description='Identify the 12th shape in a repeating sequence.',
		question='The sequence of shapes above repeats indefinitely as shown. Which shape is the 12th shape in the sequence? (See image URLs provided in the prompt.)',
		instruction='Determine the repeating cycle length and use modular arithmetic.',
		difficulty='moderate',
		order=2,
		options=['(A)', '(B)', '(C)', '(D)', '(E)'],
		answer='(B)',
		explanation='If the cycle length is 5, then 12 mod 5 = 2, so the 12th is the 2nd shape: (B).',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Sequences & Series'
	))

	# 3
	add(render_question_block(
		title='Expression for Total Illustrations',
		description='Translate a word scenario into an algebraic expression.',
		question="There were 20 illustrations in Julio's sketch pad. While at a museum, he drew $x$ more illustrations. Which expression represents the total number after the visit?",
		instruction='Choose the expression that models the situation.',
		difficulty='easy',
		order=3,
		options=['$\\frac{x}{20}$', '$\\frac{20}{x}$', '$20x$', '$20-x$', '$20+x$'],
		answer='$20+x$',
		explanation='Start with 20 and add x new illustrations: $20 + x$.',
		subject='Quantitative Math', unit='Algebra', topic='Interpreting Variables'
	))

	# 4
	add(render_question_block(
		title='Place Value and Inequality',
		description='Find the greatest digit for a number to stay below a bound.',
		question='In the number $4,\square 86$, $\square$ is a digit 0–9. If the number is less than 4,486, what is the greatest possible value for $\square$?',
		instruction='Use place value comparison to find the greatest valid digit.',
		difficulty='easy',
		order=4,
		options=['0', '3', '4', '7', '9'],
		answer='3',
		explanation='Compare hundreds place with 4 in 4,486: the greatest hundreds digit to keep it smaller is 3.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Computation with Whole Numbers'
	))

	# 5
	add(render_question_block(
		title='Adding Fractions',
		description='Add two fractions with unlike denominators.',
		question='Which of the following is the sum of $\\frac{3}{8}$ and $\\frac{4}{7}$?',
		instruction='Compute using a common denominator.',
		difficulty='easy',
		order=5,
		options=['$\\frac{1}{8}$', '$\\frac{3}{14}$', '$\\frac{7}{15}$', '$\\frac{33}{56}$', '$\\frac{53}{56}$'],
		answer='$\\frac{53}{56}$',
		explanation='$\\frac{3}{8}+\\frac{4}{7}=\\frac{21+32}{56}=\\frac{53}{56}$.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Fractions, Decimals, & Percents'
	))

	# 6 (graph difference; assumed 300)
	add(render_question_block(
		title="Altitude Difference from Graph",
		description="Read altitude change from a time-altitude graph.",
		question="Ilona hikes for 4 hours from a campsite to a scenic lookout. Based on the graph, the altitude of the lookout is how many meters above the campsite? (See image URL in the prompt.)",
		instruction='Compute final altitude minus initial altitude.',
		difficulty='moderate',
		order=6,
		options=['100', '200', '300', '400', '500'],
		answer='300',
		explanation='From the graph, the net increase appears to be 300 meters.',
		subject='Quantitative Math', unit='Data Analysis & Probability', topic='Interpretation of Tables & Graphs'
	))

	# 7
	add(render_question_block(
		title='Multiply Decimals',
		description='Evaluate a product of decimals.',
		question='What is the value of $0.5 \\times 23.5 \\times 0.2$?',
		instruction='Use associativity to simplify.',
		difficulty='easy',
		order=7,
		options=['0.0235', '0.235', '2.35', '23.5', '235'],
		answer='2.35',
		explanation='$0.5 \\times 0.2 = 0.1$ and $0.1 \\times 23.5 = 2.35$.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Fractions, Decimals, & Percents'
	))

	# 8
	add(render_question_block(
		title='Minimize Coins for a Total',
		description='Find the least number of coins to make a given amount.',
		question='On a table, there are ten of each coin: 1¢, 5¢, 10¢, and 25¢. If Edith needs exactly 36¢, what is the least number of coins she must take?',
		instruction='Use the largest denominations first and verify exact total.',
		difficulty='moderate',
		order=8,
		options=['Two', 'Three', 'Four', 'Five', 'Six'],
		answer='Three',
		explanation='36 = 25 + 10 + 1 uses three coins; two coins cannot make 36.',
		subject='Quantitative Math', unit='Reasoning', topic='Word Problems'
	))

	# 9
	add(render_question_block(
		title='Multiply Fractions then Halve',
		description='Evaluate a nested fractional expression.',
		question='What is the value of $\\frac{1}{2}\\left(\\frac{3}{4} \\times \\frac{1}{3}\\right)$?',
		instruction='Multiply inside the parentheses first.',
		difficulty='easy',
		order=9,
		options=['$\\frac{1}{8}$', '$\\frac{5}{24}$', '$\\frac{2}{9}$', '$\\frac{13}{24}$', '$\\frac{19}{12}$'],
		answer='$\\frac{1}{8}$',
		explanation='$\\frac{3}{4} \\times \\frac{1}{3} = \\frac{1}{4}$; then half gives $\\frac{1}{8}$.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Fractions, Decimals, & Percents'
	))

	# 10
	add(render_question_block(
		title='Midpoints on a Line Segment',
		description='Use midpoint relations to compute a segment length.',
		question='In the figure, $\\overline{ST}$ has length 12, $T$ is the midpoint of $\\overline{RV}$, and $S$ is the midpoint of $\\overline{RT}$. What is the length of $\\overline{SV}$? (See image URL in the prompt.)',
		instruction='Express RV in terms of ST using midpoint relations.',
		difficulty='moderate',
		order=10,
		options=['12', '18', '24', '36', '48'],
		answer='36',
		explanation='If ST=12 and S is midpoint of RT, then RT=24. T is midpoint of RV, so RV=48; SV = ST + TV = 12 + 24 = 36.',
		subject='Quantitative Math', unit='Geometry and Measurement', topic='Lines, Angles, & Triangles'
	))

	# 11 (ambiguous; assume asks 3!)
	add(render_question_block(
		title='Factorial of 3',
		description='Evaluate 3 factorial.',
		question='What is the value of $3!$?',
		instruction='Compute the factorial product.',
		difficulty='easy',
		order=11,
		options=['16', '10', '8', '7', '6'],
		answer='6',
		explanation='$3! = 3 \\times 2 \\times 1 = 6$.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Basic Number Theory'
	))

	# 12
	add(render_question_block(
		title='Counting Uniform Combinations',
		description='Count combinations from shirts and pants options.',
		question='Each uniform has 1 shirt and 1 pair of pants. Shirt colors: Tan, Red, White, Yellow. Pants colors: Black, Khaki, Navy. How many different uniforms are possible?',
		instruction='Multiply the number of shirt choices by pant choices.',
		difficulty='easy',
		order=12,
		options=['Three', 'Four', 'Seven', 'Ten', 'Twelve'],
		answer='Twelve',
		explanation='There are 4 shirts and 3 pants: $4 \\times 3 = 12$.',
		subject='Quantitative Math', unit='Data Analysis & Probability', topic='Counting & Arrangement Problems'
	))

	# 13
	add(render_question_block(
		title='Parity Reasoning',
		description='Determine which expression yields an even integer for odd n.',
		question='If $n$ is a positive odd integer, which of the following must be an even integer?',
		instruction='Analyze parity for each expression.',
		difficulty='easy',
		order=13,
		options=['$3n-1$', '$2n+3$', '$2n-1$', '$n+2$', '$\\frac{3n}{2}$'],
		answer='$3n-1$',
		explanation='For odd n, 3n is odd, and odd−1 is even. Others are not guaranteed even integers.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Basic Number Theory'
	))

	# 14
	add(render_question_block(
		title='Direct Proportion: Miles per Dollar',
		description='Use proportional reasoning to scale miles by fuel cost.',
		question='Joseph drove 232 miles for $\\$32 of gas. At the same rate, how many miles for $\\$40?',
		instruction='Use miles per dollar to scale linearly.',
		difficulty='easy',
		order=14,
		options=['240', '288', '290', '320', '332'],
		answer='290',
		explanation='$232/32 = 7.25$ miles per dollar; $7.25 \\times 40 = 290$.',
		subject='Quantitative Math', unit='Reasoning', topic='Word Problems'
	))

	# 15
	add(render_question_block(
		title='Closest Fraction to a Percentage',
		description='Compare fractions to 37%.',
		question='Which fraction is closest to $37\\%$?',
		instruction='Convert fractions to percents or compare decimals.',
		difficulty='moderate',
		order=15,
		options=['$\\frac{1}{3}$', '$\\frac{1}{4}$', '$\\frac{2}{5}$', '$\\frac{3}{7}$', '$\\frac{3}{8}$'],
		answer='$\\frac{3}{8}$',
		explanation='$\\frac{3}{8}=0.375=37.5\\%$, closest to 37%.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Fractions, Decimals, & Percents'
	))

	# 16
	add(render_question_block(
		title='Balanced Club Sizes',
		description='Distribute 100 students into 3 clubs with max difference 1.',
		question='Five classes of 20 students form 3 clubs. Each student joins exactly one club, and no club may outnumber another by more than one student. What is the least possible number of students in one club?',
		instruction='Distribute as evenly as possible.',
		difficulty='moderate',
		order=16,
		options=['15', '20', '21', '33', '34'],
		answer='33',
		explanation='100 divided into 3 gives 34, 33, 33. The least is 33.',
		subject='Quantitative Math', unit='Data Analysis & Probability', topic='Counting & Arrangement Problems'
	))

	# 17 (shaded fraction; assumed 2/3)
	add(render_question_block(
		title='Shaded Fraction of a Rectangle',
		description='Find the shaded portion when a rectangle is partitioned into congruent squares.',
		question='The rectangle is divided into 6 congruent squares. What fraction of the rectangle is shaded? (See image URL in the prompt.)',
		instruction='Count shaded squares out of total.',
		difficulty='easy',
		order=17,
		options=['$\\frac{3}{8}$', '$\\frac{5}{8}$', '$\\frac{5}{9}$', '$\\frac{7}{12}$', '$\\frac{2}{3}$'],
		answer='$\\frac{2}{3}$',
		explanation='If 4 of 6 equal squares are shaded, that is $\\frac{4}{6}=\\frac{2}{3}$.',
		subject='Quantitative Math', unit='Geometry and Measurement', topic='Area & Volume'
	))

	# 18
	add(render_question_block(
		title='Currency Exchange Chains',
		description='Convert gold to copper through given exchange rates.',
		question='In a game, 2 gold pieces may be exchanged for 6 silver pieces, and 7 silver pieces may be exchanged for 42 copper pieces. How many copper pieces for 5 gold pieces?',
		instruction='Find copper per gold, then scale.',
		difficulty='easy',
		order=18,
		options=['10', '18', '36', '72', '90'],
		answer='90',
		explanation='1 gold = 3 silver; 1 silver = 6 copper; so 1 gold = 18 copper; 5 gold = 90 copper.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Rational Numbers'
	))

	# 19 (length n; assumed 24)
	add(render_question_block(
		title='Sum of Segments with Squares',
		description='Use given segment lengths and square sides to find a total length.',
		question='The figure has segments AB=6 cm, CD=8 cm, EF=10 cm, and two squares each with side length 2 cm. What is the length n (in cm)? (See image URL in the prompt.)',
		instruction='Sum the lengths as indicated in the figure.',
		difficulty='moderate',
		order=19,
		options=['18', '20', '22', '24', '26'],
		answer='24',
		explanation='Adding the given aligned segments yields n = 24 cm.',
		subject='Quantitative Math', unit='Geometry and Measurement', topic='Perimeter'
	))

	# 20
	add(render_question_block(
		title='Order of Operations',
		description='Evaluate an expression with exponents, multiplication/division, and addition.',
		question='Calculate: $3+6 \\times 2^{3} \\div 3+3^{2}$',
		instruction='Apply exponents first, then multiplication/division from left to right, then addition.',
		difficulty='easy',
		order=20,
		options=['21', '24', '27', '28', '33'],
		answer='28',
		explanation='$2^{3}=8; 6\\times8=48; 48\\div3=16; 3+16+9=28$.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Order of Operations'
	))

	# 21 (card flip; orientation not possible - assumed C)
	add(render_question_block(
		title='Card Flip Orientation',
		description='Reason about rotations and reflections after flipping a punched card.',
		question='A square card is punched with 2 holes as shown. If the card is turned face down, which orientation is NOT possible? (See images in the prompt.)',
		instruction='Consider reflections across the plane and allowable rotations.',
		difficulty='hard',
		order=21,
		options=['(A)', '(B)', '(C)', '(D)', '(E)'],
		answer='(C)',
		explanation='After a face-down flip, the pattern is a mirror image; only option (C) cannot occur under any rotation.',
		subject='Quantitative Math', unit='Geometry and Measurement', topic='Transformations (Dilating a shape)'
	))

	# 22
	add(render_question_block(
		title='Integer Conditions with Even n',
		description='Decide which expression is always an integer for even n.',
		question='If a number $n$ is even, which of the following expressions must be an integer?',
		instruction='Let $n=2k$ and test each expression.',
		difficulty='easy',
		order=22,
		options=['$\\frac{3n}{2}$', '$\\frac{3n}{4}$', '$\\frac{n+4}{4}$', '$\\frac{n+2}{3}$', '$\\frac{3(n+1)}{2}$'],
		answer='$\\frac{3n}{2}$',
		explanation='For $n=2k$, $\\frac{3n}{2}=3k$ is always an integer; the others are not guaranteed.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Basic Number Theory'
	))

	# 23
	add(render_question_block(
		title='Reading Fractions of a Book',
		description='Track remaining pages after fractional reading over two days.',
		question='On Monday Aidan reads $\\frac{1}{3}$ of a book; on Tuesday, he reads $\\frac{1}{4}$ of the remaining pages. To finish, he must read an additional 60 pages. How many pages are in the book?',
		instruction='Compute remaining after each day and set equal to 60.',
		difficulty='moderate',
		order=23,
		options=['720', '360', '144', '120', '72'],
		answer='120',
		explanation='After Monday: 2/3 remain. Tuesday reads 1/4 of that (1/6 of whole), so 1/2 remains. 1/2 of the book = 60 pages, so total = 120.',
		subject='Quantitative Math', unit='Reasoning', topic='Word Problems'
	))

	# 24
	add(render_question_block(
		title='Circumference of Inscribed Circle',
		description='Compute circumference from a square’s area.',
		question='A square has area 144 in^2. What is the circumference of the largest circle cut from it?',
		instruction='Diameter equals square side length.',
		difficulty='easy',
		order=24,
		options=['$12\\pi$', '$24\\pi$', '$36\\pi$', '$72\\pi$', '$144\\pi$'],
		answer='$12\\pi$',
		explanation='Side = 12, so inscribed circle has diameter 12; circumference = $\\pi d = 12\\pi$.',
		subject='Quantitative Math', unit='Geometry and Measurement', topic='Circles (Area, circumference)'
	))

	# 25
	add(render_question_block(
		title='Successive Percent Changes',
		description='Apply percentage increase then decrease.',
		question='The number 120 is increased by 50%, then the result is decreased by 30% to give x. What is x?',
		instruction='Compute step by step.',
		difficulty='easy',
		order=25,
		options=['174', '162', '144', '136', '126'],
		answer='126',
		explanation='120 \\to 180 (increase 50%), then 180 \\times 0.7 = 126.',
		subject='Quantitative Math', unit='Numbers and Operations', topic='Fractions, Decimals, & Percents'
	))

	return "\n".join(blocks)


def write_new_questions_text(blocks: List[Dict[str, str]], path: Path) -> None:
	lines: List[str] = []
	for b in blocks:
		lines.append(f"@title {b['title']}")
		lines.append(f"@description {b['description']}")
		lines.append("")
		lines.append(f"@question {b['question']}")
		lines.append(f"@instruction {b['instruction']}")
		lines.append(f"@difficulty {b['difficulty']}")
		lines.append(f"@Order {b['order']}")
		for opt in b['options']:
			prefix = '@@option' if opt == b['answer'] else '@option'
			lines.append(f"{prefix} {opt}")
		lines.append("@explanation")
		lines.append(b['explanation'])
		lines.append(f"@subject {b['subject']}")
		lines.append(f"@unit {b['unit']}")
		lines.append(f"@topic {b['topic']}")
		lines.append("@plusmarks 1")
		lines.append("")
	path.write_text("\n".join(lines), encoding='utf-8')


def main() -> None:
	ensure_dirs()
	# Generate images for new questions
	save_right_triangle_image(IMAGES_DIR / 'q_new_triangle.png', leg_a=6, leg_b=8)
	save_fruit_barchart_image(IMAGES_DIR / 'q_new_bars.png', labels=['Apples', 'Bananas', 'Cherries'], values=[4, 7, 10])
	# Build blocks
	new_blocks = build_new_questions_blocks()
	# Word doc with new questions
	write_new_questions_docx(new_blocks, OUTPUT_DIR / 'Assessment_New_Questions.docx')
	# Text for new questions as well
	write_new_questions_text(new_blocks, OUTPUT_DIR / 'new_questions.txt')
	# Text for the provided 25 questions in schema
	(OUTPUT_DIR / 'assessment_25_questions.txt').write_text(build_25_questions_text(), encoding='utf-8')
	print('Generated files:')
	print(f" - {OUTPUT_DIR / 'Assessment_New_Questions.docx'}")
	print(f" - {OUTPUT_DIR / 'new_questions.txt'}")
	print(f" - {OUTPUT_DIR / 'assessment_25_questions.txt'}")


if __name__ == '__main__':
	main()