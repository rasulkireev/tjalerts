from datetime import datetime

from jobs.choices import PostSource
from jobs.utils import (
    calculate_month_over_month_change,
    calculate_year_over_year_change,
    count_of_posts_from_source_in_month,
    get_common_technology_combinations,
    get_most_in_demand_roles,
    get_new_job_titles,
    get_popular_technologies,
    get_salary_data,
    get_seniority_distribution,
    get_top_onsite_locations,
    get_work_arrangement_stats,
)


def create_hn_monthly_report():
    now = datetime.now()
    current_month = now.month - 1
    current_year = now.year

    if current_month == 0:
        current_month = 12
        current_year -= 1

    # posts
    count_of_posts = count_of_posts_from_source_in_month(PostSource.HACKER_NEWS, current_month, current_year)
    month_over_month_change = calculate_month_over_month_change(PostSource.HACKER_NEWS, current_month, current_year)
    year_over_year_change = calculate_year_over_year_change(PostSource.HACKER_NEWS, current_month, current_year)

    # job titles
    most_in_demand_roles = get_most_in_demand_roles(PostSource.HACKER_NEWS, current_month, current_year)
    seniority_distribution = get_seniority_distribution(PostSource.HACKER_NEWS, current_month, current_year)
    new_job_titles = get_new_job_titles(PostSource.HACKER_NEWS, current_month, current_year)

    # technologies
    popular_technologies = get_popular_technologies(PostSource.HACKER_NEWS, current_month, current_year)
    common_technology_combinations = get_common_technology_combinations(
        PostSource.HACKER_NEWS, current_month, current_year
    )

    # compensation
    salary_data = get_salary_data(PostSource.HACKER_NEWS, current_month, current_year)

    # location
    work_arrangement_stats = get_work_arrangement_stats(PostSource.HACKER_NEWS, current_month, current_year)
    top_onsite_locations = get_top_onsite_locations(PostSource.HACKER_NEWS, current_month, current_year)

    print(f"Count of posts: {count_of_posts}\n")
    print(f"Month over month change: {month_over_month_change}\n")
    print(f"Year over year change: {year_over_year_change}\n")
    print(f"Most in demand roles: {most_in_demand_roles}\n")
    print(f"Seniority distribution: {seniority_distribution}\n")
    print(f"New job titles: {new_job_titles}\n")
    print(f"Popular technologies: {popular_technologies}\n")
    print(f"Common technology combinations: {common_technology_combinations}\n")
    print(f"Salary data: {salary_data}\n")
    print(f"Work arrangement stats: {work_arrangement_stats}\n")

    # Ask AI to combine countries that are the same but named differently, like:
    # USA, US and U.S
    # UK, England and Great Britain
    # SF, San Francisco and Bay Area
    # NYC, New York and New York City
    # etc.
    print(f"Top onsite locations: {top_onsite_locations}\n")
