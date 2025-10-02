import streamlit as st
from collections import defaultdict

# --- Core Eligibility Logic Functions (REUSED AS-IS) ---

def check_eb1_eligibility(criteria_data):
    """
    Comprehensive EB-1 eligibility checker with ALL possible outcomes.
    EB-1A: Need 3 of 10 criteria OR 1 major award
    EB-1B: Need 2 of 6 criteria + 3 years experience + job offer
    EB-1C: Need 1 year experience + managerial role + transfer
    """
    
    # === EB-1A ASSESSMENT ===
    if criteria_data['major_award']:
        return {
            'category': 'EB-1A',
            'status': '✅ HIGHLY LIKELY',
            'score': '10/10',
            'color': '#006400', # Dark Green
            'title': 'Major Award Override - Exceptional Case',
            'details': 'You possess a major internationally recognized award (Nobel Prize, Oscar, Pulitzer Prize, Olympic Medal, Grammy, etc.). This single achievement typically satisfies all EB-1A requirements without needing additional criteria.',
            'next_steps': [
                'Gather official award documentation and certificates',
                'Compile media coverage and press releases about your award',
                'Prepare detailed impact statement of your achievement',
                'Document sustained acclaim following the award',
                'Consult with immigration attorney for petition preparation',
                'Prepare expert opinion letters highlighting award significance'
            ],
            'strength': 'EXCEPTIONAL',
            'processing': 'Self-petition possible. Very high approval rate.'
        }
    
    # Count EB-1A criteria
    eb1a_criteria_met = sum([
        criteria_data['lesser_awards'],
        criteria_data['membership'],
        criteria_data['publications'],
        criteria_data['judging'],
        criteria_data['original_contributions'],
        criteria_data['authorship'],
        criteria_data['performances'],
        criteria_data['high_salary'],
        criteria_data['commercial_success']
    ])
    
    # === EB-1B ASSESSMENT ===
    eb1b_criteria_met = sum([
        criteria_data['published_articles'],
        criteria_data['judging_research'],
        criteria_data['original_contributions_research'],
        criteria_data['tenure'] == 'yes',
        criteria_data['lesser_awards'],
        criteria_data['membership']
    ])
    
    has_eb1b_basics = (
        criteria_data['experience'] == '3_years' and
        criteria_data['offer'] == 'yes'
    )
    
    eb1b_eligible = has_eb1b_basics and eb1b_criteria_met >= 2
    
    # === EB-1C ASSESSMENT ===
    eb1c_eligible = (
        criteria_data['managerial_role'] == 'yes' and
        criteria_data['one_year_exp'] == 'yes' and
        criteria_data['transfer'] == 'yes'
    )
    
    # === ALL POSSIBLE OUTCOMES (15 Scenarios) ===
    
    # OUTCOME 1: Exceptional EB-1A (7-10 criteria)
    if eb1a_criteria_met >= 7:
        return {
            'category': 'EB-1A',
            'status': '✅ EXCEPTIONAL',
            'score': f'{eb1a_criteria_met}/10',
            'color': '#006400',
            'title': 'Extraordinary Ability - Exceptional Profile',
            'details': f'You meet {eb1a_criteria_met} of 10 EB-1A criteria (only 3 required). This is an exceptionally strong profile demonstrating sustained national or international acclaim at the very top of your field. You exceed requirements by a significant margin.',
            'next_steps': [
                'Compile comprehensive documentation for all criteria',
                'Obtain 6-10 expert opinion letters from internationally recognized leaders',
                'Prepare detailed CV with emphasis on impact and recognition',
                'Document evidence of sustained acclaim over multiple years',
                'Gather citation reports and impact metrics',
                'Engage experienced immigration attorney for premium processing',
                'Consider expedited processing given strength of case'
            ],
            'strength': 'EXCEPTIONAL',
            'processing': 'Self-petition possible. Extremely high approval probability.'
        }
    
    # OUTCOME 2: Strong EB-1A (5-6 criteria)
    if eb1a_criteria_met >= 5:
        return {
            'category': 'EB-1A',
            'status': '✅ VERY STRONG',
            'score': f'{eb1a_criteria_met}/10',
            'color': '#228B22', # Forest Green
            'title': 'Extraordinary Ability - Very Strong Profile',
            'details': f'You meet {eb1a_criteria_met} of 10 EB-1A criteria (only 3 required). This is a very strong profile with substantial evidence of extraordinary ability. You significantly exceed minimum requirements.',
            'next_steps': [
                'Document all criteria with strong evidence',
                'Obtain 5-8 expert opinion letters from field leaders',
                'Prepare comprehensive CV highlighting major achievements',
                'Compile evidence of sustained acclaim and impact',
                'Gather media coverage and recognition documentation',
                'Work with immigration attorney for strategic petition',
                'Consider self-petition for faster processing'
            ],
            'strength': 'VERY STRONG',
            'processing': 'Self-petition recommended. Very high approval rate.'
        }
    
    # OUTCOME 3: Solid EB-1A (3-4 criteria)
    if eb1a_criteria_met >= 3:
        return {
            'category': 'EB-1A',
            'status': '✅ QUALIFIED',
            'score': f'{eb1a_criteria_met}/10',
            'color': '#32CD32', # Lime Green
            'title': 'Extraordinary Ability - Meets Requirements',
            'details': f'You meet {eb1a_criteria_met} of 10 EB-1A criteria (3 required). You meet the basic requirements for EB-1A. Success depends heavily on the quality and strength of your documentation.',
            'next_steps': [
                'Focus on quality documentation for all criteria',
                'Obtain 4-6 expert opinion letters from recognized experts',
                'Prepare detailed evidence packages for each criterion',
                'Document sustained acclaim over time',
                'Review criteria you might partially meet for additional evidence',
                'Consult attorney to assess documentation strength',
                'Consider whether criteria meet "extraordinary ability" standard'
            ],
            'strength': 'QUALIFIED',
            'processing': 'Self-petition possible. Approval depends on evidence quality.'
        }
    
    # OUTCOME 4: Perfect EB-1B (6/6 criteria + requirements)
    if eb1b_eligible and eb1b_criteria_met >= 5:
        return {
            'category': 'EB-1B',
            'status': '✅ EXCEPTIONAL',
            'score': f'{eb1b_criteria_met}/6',
            'color': '#006400',
            'title': 'Outstanding Researcher/Professor - Exceptional',
            'details': f'You meet {eb1b_criteria_met} of 6 EB-1B criteria (only 2 required) plus all experience and job offer requirements. This is an outstanding academic/research profile.',
            'next_steps': [
                'Secure formal permanent job offer letter on letterhead',
                'Document 3+ years teaching/research experience clearly',
                'Compile comprehensive research achievements portfolio',
                'Obtain letters from 5-7 independent experts in your field',
                'Prepare citation reports and impact metrics',
                'Work closely with employer and attorney for petition',
                'Prepare detailed description of research contributions'
            ],
            'strength': 'EXCEPTIONAL',
            'processing': 'Employer-sponsored petition. Extremely high approval rate.'
        }
    
    # OUTCOME 5: Strong EB-1B (3-4 criteria + requirements)
    if eb1b_eligible and eb1b_criteria_met >= 3:
        return {
            'category': 'EB-1B',
            'status': '✅ VERY STRONG',
            'score': f'{eb1b_criteria_met}/6',
            'color': '#228B22',
            'title': 'Outstanding Researcher/Professor - Very Strong',
            'details': f'You meet {eb1b_criteria_met} of 6 EB-1B criteria (only 2 required) plus experience and job offer. This is a very strong academic profile.',
            'next_steps': [
                'Obtain formal permanent position offer letter',
                'Verify and document 3+ years experience thoroughly',
                'Compile all publications and research documentation',
                'Obtain letters from 4-6 independent field experts',
                'Document impact of research contributions',
                'Coordinate with employer for petition sponsorship',
                'Prepare comprehensive evidence packages'
            ],
            'strength': 'VERY STRONG',
            'processing': 'Employer-sponsored petition. Very high approval rate.'
        }
    
    # OUTCOME 6: Good EB-1B (2 criteria + requirements)
    if eb1b_eligible:
        return {
            'category': 'EB-1B',
            'status': '✅ QUALIFIED',
            'score': f'{eb1b_criteria_met}/6',
            'color': '#32CD32',
            'title': 'Outstanding Researcher/Professor - Meets Requirements',
            'details': f'You meet {eb1b_criteria_met} of 6 EB-1B criteria (2 required) with required experience and job offer. You meet the basic EB-1B requirements.',
            'next_steps': [
                'Ensure job offer is for permanent research/teaching position',
                'Verify 3+ years experience is properly documented',
                'Gather strong evidence for all criteria met',
                'Obtain letters from 3-5 independent experts',
                'Coordinate closely with employer for petition',
                'Consult attorney for petition strategy and documentation',
                'Ensure research contributions are well-documented'
            ],
            'strength': 'QUALIFIED',
            'processing': 'Employer-sponsored petition. Good approval probability.'
        }
    
    # OUTCOME 7: Perfect EB-1C
    if eb1c_eligible:
        return {
            'category': 'EB-1C',
            'status': '✅ QUALIFIED',
            'score': 'Met',
            'color': '#32CD32',
            'title': 'Multinational Manager/Executive - Qualified',
            'details': 'You meet all EB-1C requirements: 1+ year managerial/executive experience abroad with transfer to US affiliate/parent/subsidiary in similar role. This is the most straightforward EB-1 path for qualifying executives.',
            'next_steps': [
                'Document 1+ year continuous managerial employment abroad',
                'Verify US position is also managerial/executive level',
                'Confirm parent/subsidiary/affiliate corporate relationship',
                'Prepare organizational charts for foreign and US entities',
                'Document your supervisory and decision-making authority',
                'Work with employer and attorney for petition preparation',
                'Gather evidence of companies qualifying relationship'
            ],
            'strength': 'QUALIFIED',
            'processing': 'Employer-sponsored petition. Standard approval rate for qualifying cases.'
        }
    
    # OUTCOME 8: EB-1B Missing Experience
    if eb1b_criteria_met >= 2 and criteria_data['offer'] == 'yes' and criteria_data['experience'] != '3_years':
        return {
            'category': 'EB-1B',
            'status': '🟡 NEEDS EXPERIENCE',
            'score': f'{eb1b_criteria_met}/6',
            'color': '#FF8C00', # Dark Orange
            'title': 'Outstanding Researcher - Need 3 Years Experience',
            'details': f'You meet {eb1b_criteria_met} of 6 EB-1B criteria (2 required) and have a job offer, but lack the required 3 years of research/teaching experience. Once you gain sufficient experience, you should qualify.',
            'next_steps': [
                'Continue building research/teaching experience to reach 3 years',
                'Maintain job offer or secure new offer when eligible',
                'Continue strengthening research profile during waiting period',
                'Add publications and research contributions',
                'Build citation count and impact metrics',
                'Revisit EB-1B eligibility once 3-year mark is reached',
                'Consider EB-2 or EB-3 as interim pathways'
            ],
            'strength': 'NEEDS EXPERIENCE',
            'processing': 'Not yet eligible. Revisit after gaining required experience.'
        }
    
    # OUTCOME 9: EB-1B Missing Job Offer
    if eb1b_criteria_met >= 2 and criteria_data['experience'] == '3_years' and criteria_data['offer'] != 'yes':
        return {
            'category': 'EB-1B',
            'status': '🟡 NEEDS JOB OFFER',
            'score': f'{eb1b_criteria_met}/6',
            'color': '#FF8C00',
            'title': 'Outstanding Researcher - Need Permanent Job Offer',
            'details': f'You meet {eb1b_criteria_met} of 6 EB-1B criteria (2 required) and have 3+ years experience, but need a permanent research/teaching position offer from a US university or research institution.',
            'next_steps': [
                'Actively seek permanent research/teaching positions in US',
                'Apply to universities and research institutions',
                'Leverage your research profile and publications',
                'Network at academic conferences and institutions',
                'Once offer secured, proceed with EB-1B petition',
                'Consider EB-1A as alternative if outstanding achievements',
                'Maintain and strengthen research credentials during search'
            ],
            'strength': 'NEEDS JOB OFFER',
            'processing': 'Not yet eligible. Secure permanent position offer first.'
        }
    
    # OUTCOME 10: EB-1B Close (1 criterion + requirements)
    if has_eb1b_basics and eb1b_criteria_met == 1:
        return {
            'category': 'EB-1B',
            'status': '🟡 ONE CRITERION SHORT',
            'score': f'{eb1b_criteria_met}/6',
            'color': '#FF8C00',
            'title': 'Outstanding Researcher - Need One More Criterion',
            'details': f'You have experience and job offer but meet only {eb1b_criteria_met} of 6 EB-1B criteria (2 required). You need to strengthen your profile in one more area to qualify.',
            'next_steps': [
                'Review all 6 EB-1B criteria carefully for partial matches',
                'Focus on achieving one additional criterion quickly',
                'Publish additional articles in peer-reviewed journals',
                'Seek peer review opportunities in your field',
                'Apply for academic awards and recognition',
                'Join prestigious professional organizations',
                'Consult attorney to assess borderline criteria',
                'Consider EB-2 NIW as backup option'
            ],
            'strength': 'BORDERLINE',
            'processing': 'Not currently eligible. Strengthen profile before filing.'
        }
    
    # OUTCOME 11: EB-1A Borderline (2 criteria)
    if eb1a_criteria_met == 2:
        return {
            'category': 'EB-1A',
            'status': '🟡 ONE CRITERION SHORT',
            'score': f'{eb1a_criteria_met}/10',
            'color': '#FF8C00',
            'title': 'Extraordinary Ability - Need One More Criterion',
            'details': f'You meet {eb1a_criteria_met} of 10 EB-1A criteria but need 3 minimum. You are very close to qualifying. With focused effort on one additional criterion, you could become eligible.',
            'next_steps': [
                'Review all 10 criteria carefully for partial matches',
                'Focus on achieving one additional criterion',
                'Pursue awards and recognition in your field',
                'Seek judging/peer review opportunities',
                'Increase media coverage of your work',
                'Join organizations requiring outstanding achievements',
                'Document high salary if applicable',
                'Consult attorney to assess marginal criteria',
                'Consider EB-2 NIW as viable alternative',
                'Revisit EB-1A in 6-12 months'
            ],
            'strength': 'BORDERLINE',
            'processing': 'Not currently eligible. One more criterion needed.'
        }
    
    # OUTCOME 12: Dual Potential (1 EB-1A + 1 EB-1B partial)
    if eb1a_criteria_met == 1 and eb1b_criteria_met >= 1:
        paths = []
        if eb1a_criteria_met >= 1:
            paths.append(f'EB-1A ({eb1a_criteria_met}/10)')
        if eb1b_criteria_met >= 1:
            paths.append(f'EB-1B ({eb1b_criteria_met}/6)')
        
        return {
            'category': 'EB-1A/EB-1B',
            'status': '🟡 POTENTIAL',
            'score': f'{max(eb1a_criteria_met, eb1b_criteria_met)} criteria',
            'color': '#FFA500', # Orange
            'title': 'Multiple EB-1 Pathways Possible - Build Profile',
            'details': f'You show potential for multiple EB-1 pathways: {", ".join(paths)}. However, you need significantly more achievements to qualify for either category.',
            'next_steps': [
                'Choose strategic path: Academic (EB-1B) or General (EB-1A)',
                'For EB-1A: Need 2 more criteria from 10 available',
                'For EB-1B: Need qualifying criteria + experience + offer',
                'Publish in top-tier journals and conferences',
                'Build citation count and research impact',
                'Pursue awards, media coverage, and recognition',
                'Seek peer review and judging opportunities',
                'Consider EB-2 NIW as more realistic current option',
                'Revisit EB-1 eligibility in 1-2 years'
            ],
            'strength': 'DEVELOPING',
            'processing': 'Not currently eligible. Significant profile building needed.'
        }
    
    # OUTCOME 13: Weak Profile (1 criterion only)
    if eb1a_criteria_met == 1 or eb1b_criteria_met == 1:
        return {
            'category': 'EB-1',
            'status': '🟠 WEAK PROFILE',
            'score': f'1 criterion met',
            'color': '#FF6347', # Tomato
            'title': 'Not Currently Qualified - Significant Development Needed',
            'details': 'You meet only 1 EB-1 criterion. EB-1 requires substantially more achievements and recognition. You need significant career development to become competitive for this category.',
            'next_steps': [
                'Focus on long-term career development (2-3 years)',
                'Build strong publication record in respected venues',
                'Pursue multiple forms of recognition and awards',
                'Develop leadership roles in professional organizations',
                'Seek opportunities for media coverage and speaking',
                'Build citation count and measurable impact',
                'Consider EB-2 or EB-3 as more appropriate pathways',
                'Revisit EB-1 after substantial achievements',
                'Work with career mentor to build profile strategically'
            ],
            'strength': 'WEAK',
            'processing': 'Not eligible. Consider EB-2/EB-3 alternatives.'
        }
    
    # OUTCOME 14: EB-1C Only (no EB-1A/B potential)
    # Check if any EB-1C-related variable is 'yes'
    eb1c_partial = any(criteria_data[k] == 'yes' for k in ['managerial_role', 'one_year_exp', 'transfer'])
    
    if eb1a_criteria_met == 0 and eb1b_criteria_met == 0 and eb1c_partial and not eb1c_eligible:
        return {
            'category': 'EB-1C',
            'status': '🟡 PARTIAL EB-1C',
            'score': 'Incomplete',
            'color': '#FF8C00',
            'title': 'Multinational Executive - Incomplete Requirements',
            'details': 'You have some managerial/executive experience but do not meet all EB-1C requirements. EB-1A and EB-1B are not viable based on your profile.',
            'next_steps': [
                'Verify you have 1+ year managerial role with foreign entity',
                'Ensure US transfer is to parent/subsidiary/affiliate company',
                'Confirm US position is also managerial/executive level',
                'Once all requirements met, EB-1C is possible',
                'Otherwise, consider EB-2 or EB-3 categories',
                'If not in managerial track, focus on EB-2 NIW',
                'Consult attorney for alternative pathways'
            ],
            'strength': 'INCOMPLETE',
            'processing': 'Not fully eligible. Complete all EB-1C requirements.'
        }
    
    # OUTCOME 15: Not Eligible (0 criteria)
    return {
        'category': 'EB-1',
        'status': '❌ NOT ELIGIBLE',
        'score': '0 criteria',
        'color': '#DC143C', # Crimson
        'title': 'Not Qualified for EB-1 - Consider Alternative Categories',
        'details': 'Your current profile does not meet EB-1 requirements in any subcategory. EB-1 is the most selective employment-based category, reserved for those with extraordinary ability, outstanding research credentials, or multinational executive experience.',
        'next_steps': [
            'EB-1 is not appropriate at this career stage',
            'Focus on EB-2 NIW (National Interest Waiver) pathway',
            'EB-2 requires advanced degree + exceptional ability',
            'EB-3 is available for skilled workers and professionals',
            'Build career achievements for future EB-1 consideration',
            'Develop publication record and professional recognition',
            'Join professional organizations and seek leadership roles',
            'Consult attorney for EB-2/EB-3 evaluation',
            'Revisit EB-1 after 3-5 years of achievement building'
        ],
        'strength': 'NOT ELIGIBLE',
        'processing': 'EB-1 not viable. Pursue EB-2 or EB-3 categories.'
    }


# --- Streamlit UI Application ---

def display_results(result):
    """Formats and displays the eligibility result in Streamlit."""
    
    # Use HTML/Markdown for rich formatting based on result properties
    status_html = f"""
    <div style="background-color: {result['color']}; padding: 15px; border-radius: 5px; color: white; text-align: center;">
        <h2 style="margin: 0; font-size: 24px;">{result['status']}</h2>
        <p style="margin: 0; font-size: 16px;">Recommended Category: {result['category']}</p>
    </div>
    <br>
    """
    st.markdown(status_html, unsafe_allow_html=True)
    
    st.header(result['title'])
    
    col1, col2 = st.columns(2)
    with col1:
        if result['score'] != 'N/A' and result['score'] != 'Met':
            st.metric("Score", result['score'])
    with col2:
        st.metric("Strength", result['strength'])
        
    st.subheader("Assessment Details")
    st.write(result['details'])
    
    st.subheader("Processing Guidance")
    st.info(result['processing'])
    
    st.subheader("Recommended Next Steps")
    for i, step in enumerate(result['next_steps'], 1):
        st.markdown(f"**{i}.** {step}")
        
    st.markdown("---")
    st.warning("**⚠️ IMPORTANT DISCLAIMER:** This is a preliminary screening tool only and does NOT constitute legal advice. EB-1 eligibility depends on the quality and strength of documentation, not just meeting criteria. Consult with a qualified immigration attorney for a comprehensive case evaluation and petition strategy.")


def main():
    st.set_page_config(layout="wide", page_title="EB-1 Green Card Eligibility Screener")

    # Header and Layout
    st.title("🇺🇸 EB-1 Green Card Eligibility Screener")
    st.markdown("A tool to evaluate potential eligibility for the **Employment-Based First Preference (EB-1)** Green Card across three subcategories: Extraordinary Ability (EB-1A), Outstanding Researcher/Professor (EB-1B), and Multinational Manager/Executive (EB-1C).")
    st.markdown("---")
    
    # Two-column layout for input and results
    input_col, result_col = st.columns([1, 1])

    with input_col:
        st.header("1. Select Your Qualifications")
        
        # --- Collect Criteria Data ---
        criteria_data = defaultdict(lambda: False)

        # --- EB-1A Section ---
        with st.expander("🌟 EB-1A: Extraordinary Ability (Need 3 of 10 Criteria)", expanded=True):
            st.markdown("---")
            st.markdown(
                '<div style="background-color: #f7f3e8; padding: 10px; border-radius: 5px; border: 1px solid #e0c897;">'
                '**⭐ Major Award Override**'
                '</div>',
                unsafe_allow_html=True
            )
            criteria_data['major_award'] = st.checkbox("Major internationally recognized award (Nobel, Oscar, Pulitzer, Olympic Medal)", key='major_award')

            st.markdown("---")
            st.markdown("**10 EB-1A Criteria (Need a minimum of 3):**")
            
            # Using columns for the 10 criteria
            c1, c2 = st.columns(2)
            
            with c1:
                criteria_data['lesser_awards'] = st.checkbox("Lesser nationally/internationally recognized awards", key='lesser_awards')
                criteria_data['membership'] = st.checkbox("Membership requiring outstanding achievements", key='membership')
                criteria_data['publications'] = st.checkbox("Published material about you in major media", key='publications')
                criteria_data['judging'] = st.checkbox("Judged work of others (peer reviewer, panelist)", key='judging')
                criteria_data['original_contributions'] = st.checkbox("Original contributions of major significance", key='original_contributions')
            
            with c2:
                criteria_data['authorship'] = st.checkbox("Authorship of scholarly articles", key='authorship')
                criteria_data['performances'] = st.checkbox("Work displayed at exhibitions/showcases", key='performances')
                criteria_data['high_salary'] = st.checkbox("High salary or significantly high remuneration", key='high_salary')
                criteria_data['commercial_success'] = st.checkbox("Commercial success in performing arts", key='commercial_success')
                st.write("") # Placeholder for 10th criterion (often covered by Major Award or other criteria)


        # --- EB-1B Section ---
        with st.expander("🔬 EB-1B: Outstanding Researcher/Professor (Need 2 of 6 + Requirements)"):
            st.markdown("**Core Requirements:**")
            
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                criteria_data['experience'] = st.selectbox(
                    "Research/teaching experience:",
                    options=["<3_years", "3_years"],
                    format_func=lambda x: "3+ years" if x == "3_years" else "Less than 3 years",
                    key='experience'
                )
            with col_b2:
                criteria_data['offer'] = st.selectbox(
                    "Permanent US job offer:",
                    options=["no", "yes"],
                    format_func=lambda x: "Yes" if x == "yes" else "No",
                    key='offer'
                )
            with col_b3:
                criteria_data['tenure'] = st.selectbox(
                    "Tenured/permanent position:",
                    options=["no", "yes"],
                    format_func=lambda x: "Yes" if x == "yes" else "No",
                    key='tenure'
                )

            st.markdown("---")
            st.markdown("**EB-1B Criteria (Need a minimum of 2 of the following 6. Note: Some overlap with EB-1A is possible):**")
            
            criteria_data['published_articles'] = st.checkbox("Published articles in international academic journals (peer-reviewed)", key='published_articles')
            criteria_data['judging_research'] = st.checkbox("Judged research of others (peer review, grant panels)", key='judging_research')
            criteria_data['original_contributions_research'] = st.checkbox("Original research contributions of major significance to field", key='original_contributions_research')
            # Criteria shared with EB-1A are automatically collected above: lesser_awards, membership. We list them explicitly as well.
            criteria_data['lesser_awards_b'] = st.checkbox("Lesser nationally/internationally recognized awards (EB-1B specific)", key='lesser_awards_b')
            criteria_data['membership_b'] = st.checkbox("Membership requiring outstanding achievements (EB-1B specific)", key='membership_b')


        # --- EB-1C Section ---
        with st.expander("🏢 EB-1C: Multinational Manager/Executive"):
            st.markdown("**All three of the following requirements must be met:**")
            
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                criteria_data['one_year_exp'] = st.selectbox(
                    "Managerial/executive role abroad (1+ year):",
                    options=["no", "yes"],
                    format_func=lambda x: "Yes" if x == "yes" else "No",
                    key='one_year_exp'
                )
            with col_c2:
                criteria_data['transfer'] = st.selectbox(
                    "Transferring to US affiliate/parent/subsidiary:",
                    options=["no", "yes"],
                    format_func=lambda x: "Yes" if x == "yes" else "No",
                    key='transfer'
                )
            with col_c3:
                criteria_data['managerial_role'] = st.selectbox(
                    "US role is also managerial/executive:",
                    options=["no", "yes"],
                    format_func=lambda x: "Yes" if x == "yes" else "No",
                    key='managerial_role'
                )

        
        if st.button("Check Eligibility", use_container_width=True):
            # Store the data in session state before calculation
            st.session_state['criteria_data'] = criteria_data
            st.session_state['run_screener'] = True
        
    with result_col:
        st.header("2. Assessment Results")
        st.markdown("---")
        
        # Initial message
        if 'run_screener' not in st.session_state:
            st.info("Select your qualifications on the left and click **'Check Eligibility'** to receive a full assessment. This tool evaluates all 15 possible EB-1 outcomes.")
        
        # Run the screener and display results
        if st.session_state.get('run_screener', False):
            # Ensure the two EB-1B criteria that overlap with EB-1A are correctly boolean
            # The 'b' suffixes are for the UI only to avoid key conflicts, we use the main keys for logic
            criteria_data['lesser_awards'] = criteria_data.get('lesser_awards', False) or criteria_data.get('lesser_awards_b', False)
            criteria_data['membership'] = criteria_data.get('membership', False) or criteria_data.get('membership_b', False)

            result = check_eb1_eligibility(st.session_state['criteria_data'])
            display_results(result)

if __name__ == "__main__":
    main()