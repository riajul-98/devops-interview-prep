"""
Formatting utilities for consistent output
"""
import click
from typing import Dict, Any

from ..core.config import (
    EXCELLENT_THRESHOLD, 
    GOOD_THRESHOLD, 
    FAIR_THRESHOLD,
    SEPARATOR_LENGTH,
    SUMMARY_SEPARATOR_LENGTH
)


def format_separator(length: int = SEPARATOR_LENGTH) -> str:
    """Create a separator line"""
    return "=" * length


def format_percentage(value: float) -> str:
    """Format a decimal as a percentage"""
    return f"{value:.1%}"


def get_performance_emoji(success_rate: float) -> str:
    """Get emoji based on performance level"""
    if success_rate < 0.5:
        return "🔴"
    elif success_rate < 0.7:
        return "🟡"
    else:
        return "🟢"


def format_assessment(percentage: float) -> str:
    """Get assessment message based on score"""
    if percentage >= EXCELLENT_THRESHOLD:
        return "🏆 Excellent! You're interview-ready."
    elif percentage >= GOOD_THRESHOLD:
        return "🎉 Great work! You're well-prepared."
    elif percentage >= FAIR_THRESHOLD:
        return "👍 Good progress. Focus on weak areas."
    else:
        return "📚 More preparation needed. Keep practicing!"


def format_duration(seconds: int) -> str:
    """Format duration in a readable format"""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds}s"


def print_header(title: str, emoji: str = "📊"):
    """Print a formatted header"""
    click.echo(f"{emoji} {title.upper()}")
    click.echo(format_separator(len(title) + 5))


def print_section_header(title: str):
    """Print a section header"""
    click.echo(f"\n{title}:")


def print_weak_areas_list(weak_areas: list):
    """Print formatted weak areas list"""
    click.echo("🎯 Areas needing improvement (lowest success rates):")
    click.echo(format_separator(50))
    
    for i, (topic, success_rate) in enumerate(weak_areas, 1):
        emoji = get_performance_emoji(success_rate)
        click.echo(f"{i}. {emoji} {topic}: {format_percentage(success_rate)} success rate")


def print_analytics_summary(stats: Dict[str, Any]):
    """Print formatted analytics summary"""
    print_header("PERFORMANCE ANALYTICS", "📈")
    click.echo(f"📊 Total questions attempted: {stats['total_attempted']}")
    click.echo(f"🎯 Overall success rate: {format_percentage(stats['success_rate'])}")
    click.echo(f"🔥 Recent performance (last 10): {format_percentage(stats['recent_success_rate'])}")


def print_topic_stats(topic_stats: dict):
    """Print formatted topic statistics"""
    print_section_header("📚 Performance by topic")
    for topic_name, stats in sorted(topic_stats.items()):
        rate = stats['correct'] / stats['total']
        emoji = get_performance_emoji(rate)
        click.echo(f"  {emoji} {topic_name}: {stats['correct']}/{stats['total']} ({format_percentage(rate)})")


def print_difficulty_stats(difficulty_stats: dict):
    """Print formatted difficulty statistics"""
    print_section_header("🎚️  Performance by difficulty")
    for diff, stats in sorted(difficulty_stats.items()):
        rate = stats['correct'] / stats['total']
        emoji = get_performance_emoji(rate)
        click.echo(f"  {emoji} {diff}: {stats['correct']}/{stats['total']} ({format_percentage(rate)})")