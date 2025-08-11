"""
Review mistakes command
"""
import click
from ..core.progress_tracker import progress_tracker
from ..core.question_bank import question_bank
from ..models.session import InterviewSession
from ..core.config import DEFAULT_REVIEW_COUNT


@click.command()
@click.option('--count', '-c', default=DEFAULT_REVIEW_COUNT, help='Maximum number of questions to review')
def review_mistakes(count):
    """🔄 Review questions you got wrong"""
    failed_ids = progress_tracker.get_failed_questions()
    
    if not failed_ids:
        click.echo("🎉 No incorrect answers found. Great job!")
        click.echo("💡 Keep practicing to maintain your performance!")
        return
    
    click.echo(f"📚 Found {len(failed_ids)} questions to review")
    
    # Limit the number of questions to review
    review_count = min(count, len(failed_ids))
    questions = question_bank.get_questions(question_ids=failed_ids[:review_count])
    
    if not questions:
        click.echo("❌ Could not find the failed questions")
        return
    
    click.echo(f"🔄 Reviewing {len(questions)} previously missed questions")
    
    session = InterviewSession()
    
    for i, question in enumerate(questions, 1):
        click.echo(f"\n📋 Review Question {i}/{len(questions)}")
        session.ask_question(question)
    
    session.show_summary()