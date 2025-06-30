from pdf2image import convert_from_path

pages = convert_from_path(r"D:/Em yêu những môn học này/OOP/Mascarade/55-mascarade-rulebook.pdf")
for i, page in enumerate(pages):
    page.save(f'rulebook_page_{i+1}.png', 'PNG')