import random
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter, A4, legal
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate

# Function to read questions from a file
def read_questions_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions = [line.strip() for line in f if line.strip()]
        return questions
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except UnicodeDecodeError:
        print(f"Error: Failed to decode file '{filename}' using UTF-8 encoding. Please ensure the file is saved with UTF-8 encoding.")
        return []

def generate_cards(total_cards, truth_questions, dare_questions):
    """
    Generates a list of (category, question) tuples.
    Total cards must be even.
    """
    if total_cards % 2 != 0:
        raise ValueError("Total number of cards must be even.")
    num_each = total_cards // 2

    # Calculate how many copies of each list we need
    truth_copies = (num_each // len(truth_questions)) + 1
    dare_copies = (num_each // len(dare_questions)) + 1
    
    truth_pool = truth_questions * truth_copies
    dare_pool = dare_questions * dare_copies

    selected_truths = random.sample(truth_pool, num_each)
    selected_dares = random.sample(dare_pool, num_each)

    cards = [("TRUTH", q) for q in selected_truths] + [("DARE", q) for q in selected_dares]
    random.shuffle(cards)
    return cards

def choose_paper_size():
    """
    Lets the user choose a standard paper size.
    """
    sizes = {
        "1": ("Letter", letter),
        "2": ("A4", A4),
        "3": ("Legal", legal)
    }
    print("\nChoose a paper size:")
    print("1: Letter (8.5 x 11 in)")
    print("2: A4 (210 x 297 mm)")
    print("3: Legal (8.5 x 14 in)")
    
    while True:
        choice = input("Enter the number corresponding to your choice [1]: ").strip()
        if not choice:  # Default to letter if no input
            choice = "1"
        if choice in sizes:
            print(f"Selected {sizes[choice][0]} paper.")
            return sizes[choice][1]
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def get_card_dimensions():
    """
    Lets the user customize card dimensions with defaults.
    """
    print("\nCard dimensions (standard playing card is about 2.5\" x 3.5\"):")
    
    try:
        width = input("Enter card width in inches [1.5]: ").strip()
        width = float(width) if width else 1.5
        
        height = input("Enter card height in inches [2.5]: ").strip()
        height = float(height) if height else 2.5
        
        if width <= 0 or height <= 0:
            print("Dimensions must be positive. Using defaults (1.5\" x 2.5\").")
            return 1.5 * inch, 2.5 * inch
        
        return width * inch, height * inch
    except ValueError:
        print("Invalid input. Using default dimensions (1.5\" x 2.5\").")
        return 1.5 * inch, 2.5 * inch

def draw_cards_to_pdf(cards, paper_size, output_filename, card_width, card_height):
    """
    Draws the list of cards on a PDF.
    Each card is drawn as a rectangle with text inside.
    """
    try:
        c = canvas.Canvas(output_filename, pagesize=paper_size)
        page_width, page_height = paper_size

        margin = 0.5 * inch
        available_width = page_width - 2 * margin
        available_height = page_height - 2 * margin

        cols = int(available_width // card_width)
        rows = int(available_height // card_height)
        cards_per_page = rows * cols
        
        if cards_per_page == 0:
            print("Warning: Paper size too small for the selected card dimensions.")
            print("Adjusting card size to fit at least one card per page.")
            
            # Adjust card size to fit at least one per page
            card_width = min(card_width, available_width)
            card_height = min(card_height, available_height)
            cols = max(1, int(available_width // card_width))
            rows = max(1, int(available_height // card_height))
            cards_per_page = rows * cols

        card_index = 0
        total_cards = len(cards)
        total_pages = (total_cards + cards_per_page - 1) // cards_per_page
        
        print(f"\nGenerating {total_cards} cards across {total_pages} pages...")
        
        # Define consistent fonts - using standard fonts that come with ReportLab
        font_regular = "Helvetica"
        font_bold = "Helvetica-Bold"
        
        while card_index < total_cards:
            for row in range(rows):
                for col in range(cols):
                    if card_index >= total_cards:
                        break
                    x = margin + col * card_width
                    y = page_height - margin - (row + 1) * card_height

                    # Draw the card border
                    c.rect(x, y, card_width, card_height)

                    qtype, question = cards[card_index]
                    
                    # Use direct canvas drawing instead of Paragraph
                    # Draw border line
                    c.setStrokeColorRGB(0.8, 0.8, 0.8)
                    c.line(x + 10, y + card_height - 15, x + card_width - 10, y + card_height - 15)
                    
                    # Draw title
                    c.setFont(font_bold, 14)
                    if qtype == "TRUTH":
                        c.setFillColorRGB(0, 0, 1)  # Blue
                        title_text = "🤫 TRUTH"
                    else:
                        c.setFillColorRGB(1, 0, 0)  # Red
                        title_text = "😈 DARE"
                    
                    # Center the title
                    title_width = c.stringWidth(title_text, font_bold, 14)
                    c.drawString(x + (card_width - title_width) / 2, y + card_height - 30, title_text)
                    
                    # Draw question
                    c.setFont(font_bold, 10)
                    c.setFillColorRGB(0, 0, 0)  # Black
                    
                    # Handle long questions - split into multiple lines if needed
                    max_width = card_width - 20  # 10pt padding on each side
                    
                    # Split text into words
                    words = question.split()
                    lines = []
                    current_line = []
                    
                    for word in words:
                        test_line = ' '.join(current_line + [word])
                        if c.stringWidth(test_line, font_bold, 10) <= max_width:
                            current_line.append(word)
                        else:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    # Calculate vertical position for text block
                    line_height = 12  # points
                    text_block_height = len(lines) * line_height
                    text_y = y + (card_height - text_block_height) / 2 + text_block_height
                    
                    # Draw each line of text
                    for line in lines:
                        line_width = c.stringWidth(line, font_bold, 10)
                        text_y -= line_height
                        c.drawString(x + (card_width - line_width) / 2, text_y, line)
                    
                    # Draw bottom line
                    c.setStrokeColorRGB(0.8, 0.8, 0.8)
                    c.line(x + 10, y + 15, x + card_width - 10, y + 15)
                    
                    card_index += 1
                if card_index >= total_cards:
                    break
            
            # Add page number at the bottom
            c.setFont(font_regular, 8)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(page_width/2 - 20, margin/2, f"Page {c.getPageNumber()} of {total_pages}")
            
            c.showPage()
        
        c.save()
        print(f"\nSuccess! PDF saved as '{output_filename}'.")
        print("Print the PDF, cut along the card outlines, and enjoy your game!")
        
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")

def main():
    import os
    # Set the current working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("===== Truth or Dare Card Generator =====")
    print("This program creates printable Truth or Dare cards for your next party!")
    
    # Load questions from files
    print("Loading questions from files...")
    truth_questions = read_questions_from_file('truth_questions.txt')
    dare_questions = read_questions_from_file('dare_questions.txt')

    if not truth_questions:
        print("Error: No truth questions found. Please provide 'truth_questions.txt' with questions.")
        return

    if not dare_questions:
        print("Error: No dare questions found. Please provide 'dare_questions.txt' with questions.")
        return

    # Get number of cards
    while True:
        try:
            total_cards_input = input("\nEnter total number of cards (must be an even number) [50]: ").strip()
            total_cards_input = int(total_cards_input) if total_cards_input else 50
            
            if total_cards_input <= 0:
                print("Number must be positive.")
                continue
                
            if total_cards_input % 2 != 0:
                print("Number is not even. Adding 1 to make it even.")
                total_cards_input += 1
                
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Choose paper size
    paper_size = choose_paper_size()
    
    # Get card dimensions
    card_width, card_height = get_card_dimensions()
    
    # Generate cards with loaded questions
    try:
        cards = generate_cards(total_cards_input, truth_questions, dare_questions)
    except Exception as e:
        print(f"Error generating cards: {str(e)}")
        return
    
    # Get output filename
    while True:
        output_filename = input("\nEnter output PDF filename [truth_or_dare.pdf]: ").strip()
        if not output_filename:
            output_filename = "truth_or_dare.pdf"
        if not output_filename.endswith(".pdf"):
            output_filename += ".pdf"
            
        # Check if file already exists
        if os.path.exists(output_filename):
            overwrite = input(f"File '{output_filename}' already exists. Overwrite? (y/n): ").lower()
            if overwrite == 'y':
                break
        else:
            break
    
    # Create the PDF
    draw_cards_to_pdf(cards, paper_size, output_filename, card_width, card_height)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    finally:
        print("\nThank you for using the Truth or Dare Card Generator!")