#!/usr/bin/env python3
"""
DevOps Interview Prep CLI - Interactive Interview Practice Tool with Progress Tracking
"""

import json
import click
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import random as py_random

@dataclass
class Question:
    id: str
    topic: str
    difficulty: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    scenario: Optional[str] = None
    company_tags: Optional[List[str]] = None
    real_world_context: Optional[str] = None

@dataclass
class QuestionResult:
    question_id: str
    topic: str
    difficulty: str
    correct: bool
    timestamp: datetime
    time_taken: Optional[float] = None

class ProgressTracker:
    def __init__(self):
        self.results_file = Path.home() / ".devops-ip" / "progress.json"
        self.results_file.parent.mkdir(exist_ok=True)
        self.results = self._load_results()
    
    def _load_results(self) -> List[QuestionResult]:
        if not self.results_file.exists():
            return []
        
        try:
            with open(self.results_file, 'r') as f:
                data = json.load(f)
            return [
                QuestionResult(
                    question_id=r['question_id'],
                    topic=r['topic'], 
                    difficulty=r['difficulty'],
                    correct=r['correct'],
                    timestamp=datetime.fromisoformat(r['timestamp']),
                    time_taken=r.get('time_taken')
                )
                for r in data
            ]
        except Exception:
            return []
    
    def save_result(self, result: QuestionResult):
        self.results.append(result)
        try:
            with open(self.results_file, 'w') as f:
                json.dump([
                    {
                        'question_id': r.question_id,
                        'topic': r.topic,
                        'difficulty': r.difficulty,
                        'correct': r.correct,
                        'timestamp': r.timestamp.isoformat(),
                        'time_taken': r.time_taken
                    }
                    for r in self.results
                ], f, indent=2)
        except Exception as e:
            click.echo(f"⚠️  Warning: Could not save progress: {e}")
    
    def get_weak_areas(self) -> List[Tuple[str, float]]:
        """Get topics with lowest success rates"""
        topic_stats = {}
        for result in self.results:
            if result.topic not in topic_stats:
                topic_stats[result.topic] = {'correct': 0, 'total': 0}
            topic_stats[result.topic]['total'] += 1
            if result.correct:
                topic_stats[result.topic]['correct'] += 1
        
        weak_areas = []
        for topic, stats in topic_stats.items():
            if stats['total'] >= 3:
                success_rate = stats['correct'] / stats['total']
                weak_areas.append((topic, success_rate))
        
        return sorted(weak_areas, key=lambda x: x[1])[:5]
    
    def get_failed_questions(self) -> List[str]:
        """Get IDs of questions that were answered incorrectly"""
        failed = []
        for result in self.results:
            if not result.correct:
                failed.append(result.question_id)
        return list(set(failed))

class InterviewQuestionBank:
    def __init__(self, questions_file: str = "questions/interview_questions.json"):
        self.questions_file = Path(questions_file)
        self.questions: List[Question] = []
        self.load_questions()
    
    def load_questions(self):
        """Load interview questions from JSON file"""
        if not self.questions_file.exists():
            click.echo(f"❌ Error: Questions file not found: {self.questions_file}")
            return
        
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.questions = []
            for q_data in data.get('questions', []):
                question = Question(
                    id=q_data['id'],
                    topic=q_data['topic'],
                    difficulty=q_data['difficulty'],
                    question=q_data['question'],
                    options=q_data['options'],
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data['explanation'],
                    scenario=q_data.get('scenario'),
                    company_tags=q_data.get('company_tags', []),
                    real_world_context=q_data.get('real_world_context')
                )
                self.questions.append(question)
            
            click.echo(f"✅ Loaded {len(self.questions)} interview questions")
        except Exception as e:
            click.echo(f"❌ Error loading questions: {e}")
    
    def get_questions(self, topic: Optional[str] = None, difficulty: Optional[str] = None, 
                     count: int = 1, company_type: Optional[str] = None,
                     question_ids: Optional[List[str]] = None) -> List[Question]:
        """Get filtered questions based on criteria"""
        filtered = self.questions
        
        if question_ids:
            filtered = [q for q in filtered if q.id in question_ids]
        
        if topic:
            filtered = [q for q in filtered if q.topic.lower() == topic.lower()]
        
        if difficulty:
            filtered = [q for q in filtered if q.difficulty.lower() == difficulty.lower()]
        
        if company_type:
            filtered = [q for q in filtered if company_type.lower() in [tag.lower() for tag in (q.company_tags or [])]]
        
        if not filtered:
            return []
        
        return py_random.sample(filtered, min(count, len(filtered)))
    
    def get_topics(self) -> List[str]:
        return sorted(list(set(q.topic for q in self.questions)))
    
    def get_company_types(self) -> List[str]:
        company_types = set()
        for q in self.questions:
            if q.company_tags:
                company_types.update(q.company_tags)
        return sorted(list(company_types))

class InterviewSession:
    def __init__(self, track_progress: bool = True):
        self.score = 0
        self.total = 0
        self.start_time = datetime.now()
        self.topic_performance = {}
        self.track_progress = track_progress
        self.results = []
    
    def ask_question(self, question: Question) -> bool:
        """Ask an interview question and return if answer was correct"""
        click.echo("\n" + "="*70)
        
        if question.scenario:
            click.echo(f"📋 Scenario: {question.scenario}")
            click.echo()
        
        click.echo(f"❓ Question: {question.question}")
        click.echo()
        
        original_correct_answer = question.correct_answer
        original_options = question.options.copy()
        
        options_with_correctness = [(option, i+1 == original_correct_answer) for i, option in enumerate(original_options)]
        py_random.shuffle(options_with_correctness)
        
        new_correct_position = None
        shuffled_options = []
        for i, (option_text, is_correct) in enumerate(options_with_correctness):
            shuffled_options.append(option_text)
            if is_correct:
                new_correct_position = i + 1
        
        for i, option in enumerate(shuffled_options, 1):
            click.echo(f"   {i}. {option}")
        
        click.echo()
        
        question_start_time = datetime.now()
        
        while True:
            try:
                answer = click.prompt("Your answer (1-{})".format(len(shuffled_options)), type=int)
                if 1 <= answer <= len(shuffled_options):
                    break
                else:
                    click.echo(f"Please enter a number between 1 and {len(shuffled_options)}")
            except click.Abort:
                return False
            except:
                click.echo("Please enter a valid number")
        
        time_taken = (datetime.now() - question_start_time).total_seconds()
        
        self.total += 1
        correct = answer == new_correct_position
        
        if question.topic not in self.topic_performance:
            self.topic_performance[question.topic] = {'correct': 0, 'total': 0}
        self.topic_performance[question.topic]['total'] += 1
        
        if correct:
            self.score += 1
            self.topic_performance[question.topic]['correct'] += 1
            click.echo("✅ Correct!")
        else:
            correct_answer_text = original_options[original_correct_answer - 1]
            click.echo(f"❌ Incorrect. Correct answer: {correct_answer_text}")
        
        click.echo(f"💡 Explanation: {question.explanation}")
        
        if question.real_world_context:
            click.echo(f"🌍 Real-world context: {question.real_world_context}")
        
        if self.track_progress:
            result = QuestionResult(
                question_id=question.id,
                topic=question.topic,
                difficulty=question.difficulty,
                correct=correct,
                timestamp=datetime.now(),
                time_taken=time_taken
            )
            progress_tracker.save_result(result)
            self.results.append(result)
        
        return correct
    
    def show_summary(self):
        """Show interview session summary"""
        duration = datetime.now() - self.start_time
        percentage = (self.score / self.total * 100) if self.total > 0 else 0
        
        click.echo("\n" + "="*50)
        click.echo("📊 SESSION SUMMARY")
        click.echo("="*50)
        click.echo(f"Score: {self.score}/{self.total} ({percentage:.1f}%)")
        click.echo(f"Duration: {duration.seconds // 60}m {duration.seconds % 60}s")
        
        if self.topic_performance:
            click.echo("\n📈 Performance by Topic:")
            for topic, perf in sorted(self.topic_performance.items()):
                topic_pct = (perf['correct'] / perf['total'] * 100) if perf['total'] > 0 else 0
                click.echo(f"  {topic}: {perf['correct']}/{perf['total']} ({topic_pct:.0f}%)")
        
        click.echo(f"\n🎯 Assessment:")
        if percentage >= 90:
            click.echo("🏆 Excellent! You're interview-ready.")
        elif percentage >= 75:
            click.echo("🎉 Great work! You're well-prepared.")
        elif percentage >= 60:
            click.echo("👍 Good progress. Focus on weak areas.")
        else:
            click.echo("📚 More preparation needed. Keep practicing!")
    
    def export_results(self, filename: str):
        """Export session results to JSON file"""
        if not self.results:
            click.echo("No results to export")
            return
        
        try:
            export_data = {
                'session_summary': {
                    'score': self.score,
                    'total': self.total,
                    'percentage': (self.score / self.total * 100) if self.total > 0 else 0,
                    'duration_seconds': (datetime.now() - self.start_time).total_seconds()
                },
                'results': [asdict(r) for r in self.results]
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            click.echo(f"📄 Results exported to {filename}")
        except Exception as e:
            click.echo(f"❌ Error exporting results: {e}")

# Initialize components
question_bank = InterviewQuestionBank()
progress_tracker = ProgressTracker()

@click.group()
@click.version_option(version="1.1.0")
def cli():
    """🚀 DevOps Interview Prep - Master Your Next DevOps Interview

    Practice AWS, Kubernetes, Docker, Linux, Git, Networking, Terraform, CI/CD,
    Security, and Monitoring with real interview questions!
    
    💡 New Features:
    • Progress tracking and weak area identification
    • Review missed questions
    • Detailed performance analytics
    • Export results for further analysis
    """
    pass

@cli.command()
@click.argument('topic', required=False)
@click.option('--difficulty', '-d', help='Difficulty level (easy, medium, hard)')
@click.option('--count', '-c', default=5, help='Number of questions')
@click.option('--company-type', help='Company type (faang, startup, enterprise)')
@click.option('--interview-mode', '-i', is_flag=True, help='Interview simulation mode')
@click.option('--export', help='Export results to JSON file')
def practice(topic, difficulty, count, company_type, interview_mode, export):
    """Practice interview questions by topic"""
    
    if not question_bank.questions:
        click.echo("❌ Error: No questions available")
        return
    
    if not topic:
        topics = question_bank.get_topics()
        click.echo("📚 Available topics:")
        for t in topics:
            topic_count = len([q for q in question_bank.questions if q.topic == t])
            click.echo(f"  • {t} ({topic_count} questions)")
        topic = click.prompt("\nSelect a topic", type=click.Choice(topics, case_sensitive=False))
    
    questions = question_bank.get_questions(topic, difficulty, count, company_type)
    
    if not questions:
        click.echo(f"❌ No questions found for the specified criteria")
        return
    
    click.echo(f"\n🎯 Starting practice: {topic.upper()}")
    if difficulty:
        click.echo(f"📊 Difficulty: {difficulty}")
    if company_type:
        click.echo(f"🏢 Company type: {company_type}")
    click.echo(f"📝 Questions: {len(questions)}")
    
    session = InterviewSession()
    
    for i, question in enumerate(questions, 1):
        click.echo(f"\n📋 Question {i}/{len(questions)} | {question.difficulty.upper()}")
        session.ask_question(question)
        
        if interview_mode and i < len(questions):
            if not click.confirm("\nContinue to next question?", default=True):
                break
    
    session.show_summary()
    
    if export:
        session.export_results(export)

@cli.command()
def weak_areas():
    """🎯 Show topics where you need more practice"""
    weak_areas = progress_tracker.get_weak_areas()
    
    if not weak_areas:
        click.echo("📊 No performance data available yet.")
        click.echo("💡 Practice some questions first to see your weak areas!")
        
        if question_bank.questions:
            topics = question_bank.get_topics()
            suggested_topic = topics[0] if topics else None
            if suggested_topic and click.confirm(f"\nStart practicing {suggested_topic}?"):
                ctx = click.get_current_context()
                ctx.invoke(practice, topic=suggested_topic, count=5)
        return
    
    click.echo("🎯 Areas needing improvement (lowest success rates):")
    click.echo("="*50)
    
    for i, (topic, success_rate) in enumerate(weak_areas, 1):
        emoji = "🔴" if success_rate < 0.5 else "🟡" if success_rate < 0.7 else "🟢"
        click.echo(f"{i}. {emoji} {topic}: {success_rate:.1%} success rate")
    
    if weak_areas:
        click.echo(f"\n💡 Recommendation: Focus on {weak_areas[0][0]}")
        if click.confirm(f"Practice {weak_areas[0][0]} questions now?"):
            ctx = click.get_current_context()
            ctx.invoke(practice, topic=weak_areas[0][0], count=5)

@cli.command()
@click.option('--count', '-c', default=10, help='Maximum number of questions to review')
def review_mistakes():
    """🔄 Review questions you got wrong"""
    failed_ids = progress_tracker.get_failed_questions()
    
    if not failed_ids:
        click.echo("🎉 No incorrect answers found. Great job!")
        click.echo("💡 Keep practicing to maintain your performance!")
        return
    
    click.echo(f"📚 Found {len(failed_ids)} questions to review")
    
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

@cli.command()
@click.option('--topic', help='Show analytics for specific topic')
@click.option('--export', help='Export analytics to JSON file')
def analytics(topic, export):
    """📈 Show detailed performance analytics"""
    results = progress_tracker.results
    
    if not results:
        click.echo("📊 No performance data available yet.")
        click.echo("💡 Practice some questions first to see your analytics!")
        return
    
    if topic:
        results = [r for r in results if r.topic.lower() == topic.lower()]
        if not results:
            click.echo(f"❌ No data found for topic: {topic}")
            return
    
    total = len(results)
    correct = sum(1 for r in results if r.correct)
    success_rate = correct / total
    
    click.echo("📈 PERFORMANCE ANALYTICS")
    click.echo("="*40)
    click.echo(f"📊 Total questions attempted: {total}")
    click.echo(f"🎯 Overall success rate: {success_rate:.1%}")
    
    recent_results = results[-10:]
    recent_correct = sum(1 for r in recent_results if r.correct)
    recent_rate = recent_correct / len(recent_results) if recent_results else 0
    click.echo(f"🔥 Recent performance (last {len(recent_results)}): {recent_rate:.1%}")
    
    topic_stats = {}
    for result in results:
        if result.topic not in topic_stats:
            topic_stats[result.topic] = {'correct': 0, 'total': 0}
        topic_stats[result.topic]['total'] += 1
        if result.correct:
            topic_stats[result.topic]['correct'] += 1
    
    click.echo(f"\n📚 Performance by topic:")
    for topic_name, stats in sorted(topic_stats.items()):
        rate = stats['correct'] / stats['total']
        emoji = "🔴" if rate < 0.5 else "🟡" if rate < 0.7 else "🟢"
        click.echo(f"  {emoji} {topic_name}: {stats['correct']}/{stats['total']} ({rate:.1%})")
    
    difficulty_stats = {}
    for result in results:
        if result.difficulty not in difficulty_stats:
            difficulty_stats[result.difficulty] = {'correct': 0, 'total': 0}
        difficulty_stats[result.difficulty]['total'] += 1
        if result.correct:
            difficulty_stats[result.difficulty]['correct'] += 1
    
    if difficulty_stats:
        click.echo(f"\n🎚️  Performance by difficulty:")
        for diff, stats in sorted(difficulty_stats.items()):
            rate = stats['correct'] / stats['total']
            emoji = "🔴" if rate < 0.5 else "🟡" if rate < 0.7 else "🟢"
            click.echo(f"  {emoji} {diff}: {stats['correct']}/{stats['total']} ({rate:.1%})")
    
    if export:
        analytics_data = {
            'summary': {
                'total_questions': total,
                'overall_success_rate': success_rate,
                'recent_success_rate': recent_rate
            },
            'by_topic': {topic: {'success_rate': stats['correct']/stats['total'], 'total': stats['total']} 
                        for topic, stats in topic_stats.items()},
            'by_difficulty': {diff: {'success_rate': stats['correct']/stats['total'], 'total': stats['total']} 
                             for diff, stats in difficulty_stats.items()}
        }
        
        try:
            with open(export, 'w') as f:
                json.dump(analytics_data, f, indent=2)
            click.echo(f"\n📄 Analytics exported to {export}")
        except Exception as e:
            click.echo(f"❌ Error exporting analytics: {e}")

@cli.command()
def topics():
    """📚 List all available interview topics"""
    topics = question_bank.get_topics()
    company_types = question_bank.get_company_types()
    
    if not topics:
        click.echo("❌ No topics available")
        return
    
    click.echo("📚 Available interview topics:")
    click.echo("="*35)
    
    for topic in topics:
        count = len([q for q in question_bank.questions if q.topic == topic])
        difficulties = set(q.difficulty for q in question_bank.questions if q.topic == topic)
        diff_str = ", ".join(sorted(difficulties))
        click.echo(f"  • {topic}: {count} questions ({diff_str})")
    
    if company_types:
        click.echo(f"\n🏢 Company types: {', '.join(company_types)}")

@cli.command()
@click.option('--count', '-c', default=15, help='Number of questions')
@click.option('--company-type', help='Focus on specific company type')
@click.option('--duration', help='Time limit (e.g., 45min)')
@click.option('--export', help='Export interview results to JSON file')
def interview(count, company_type, duration, export):
    """🎭 Full interview simulation with mixed topics"""
    if not question_bank.questions:
        click.echo("❌ Error: No questions available")
        return
    
    all_questions = question_bank.questions
    if company_type:
        all_questions = [q for q in all_questions if company_type.lower() in [tag.lower() for tag in (q.company_tags or [])]]
    
    if len(all_questions) < count:
        count = len(all_questions)
        click.echo(f"⚠️  Adjusted to {count} questions (all available)")
    
    selected_questions = py_random.sample(all_questions, count)
    
    click.echo("🎭 INTERVIEW SIMULATION")
    click.echo("="*30)
    click.echo(f"📝 Questions: {count}")
    if company_type:
        click.echo(f"🏢 Company type: {company_type}")
    if duration:
        click.echo(f"⏱️  Time limit: {duration}")
    
    topic_dist = {}
    for q in selected_questions:
        topic_dist[q.topic] = topic_dist.get(q.topic, 0) + 1
    
    click.echo(f"\n📊 Question distribution:")
    for topic, cnt in sorted(topic_dist.items()):
        click.echo(f"  • {topic}: {cnt}")
    
    if not click.confirm("\n🚀 Ready to begin your interview?"):
        return
    
    session = InterviewSession()
    
    for i, question in enumerate(selected_questions, 1):
        click.echo(f"\n🎯 Interview Question {i}/{count}")
        click.echo(f"📚 Topic: {question.topic} | 📊 Difficulty: {question.difficulty}")
        session.ask_question(question)
    
    session.show_summary()
    
    if export:
        session.export_results(export)

@cli.command()
def stats():
    """📊 Show question bank and progress statistics"""
    if not question_bank.questions:
        click.echo("❌ No questions available")
        return
    
    total = len(question_bank.questions)
    topics = question_bank.get_topics()
    
    click.echo("📊 QUESTION BANK STATISTICS")
    click.echo("="*35)
    click.echo(f"📝 Total questions: {total}")
    click.echo(f"📚 Topics: {len(topics)}")
    
    diff_dist = {}
    for q in question_bank.questions:
        diff_dist[q.difficulty] = diff_dist.get(q.difficulty, 0) + 1
    
    click.echo(f"\n🎚️  By difficulty:")
    for difficulty in ['easy', 'medium', 'hard']:
        if difficulty in diff_dist:
            click.echo(f"  • {difficulty}: {diff_dist[difficulty]}")
    
    click.echo(f"\n📚 By topic:")
    for topic in sorted(topics):
        count = len([q for q in question_bank.questions if q.topic == topic])
        click.echo(f"  • {topic}: {count}")
    
    if progress_tracker.results:
        total_attempted = len(progress_tracker.results)
        total_correct = sum(1 for r in progress_tracker.results if r.correct)
        overall_rate = total_correct / total_attempted if total_attempted > 0 else 0
        
        click.echo(f"\n📈 YOUR PROGRESS:")
        click.echo(f"  • Questions attempted: {total_attempted}")
        click.echo(f"  • Overall success rate: {overall_rate:.1%}")
        click.echo(f"  • Questions remaining: {total - len(set(r.question_id for r in progress_tracker.results))}")

@cli.command()
def quick():
    """⚡ Get a single random question for quick practice"""
    if not question_bank.questions:
        click.echo("❌ No questions available")
        return
    
    question = py_random.choice(question_bank.questions)
    
    click.echo("⚡ QUICK PRACTICE")
    click.echo("="*20)
    
    session = InterviewSession()
    session.ask_question(question)
    
    click.echo(f"\n⚡ Quick result: {session.score}/{session.total}")

if __name__ == '__main__':
    cli()