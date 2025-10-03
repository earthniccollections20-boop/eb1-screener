import streamlit as st
from collections import defaultdict
from fpdf import FPDF
import io

# --- PDF Generation ---
def generate_pdf(criteria_data, result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="EB-1 Eligibility Assessment Report", ln=True, align='C')
    pdf.ln(10)

    # User Responses
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="User Responses:", ln=True)
    pdf.set_font("Arial", size=11)
    for key, value in criteria_data.items():
        pdf.cell(200, 8, txt=f"{key.replace('_', ' ').title()}: {value}", ln=True)

    pdf.ln(10)

    # Assessment Result
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Assessment Result:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, f"Category: {result['category']}\nStatus: {result['status']}\nScore: {result['score']}\nStrength: {result['strength']}\n\nDetails:\n{result['details']}\n\nProcessing:\n{result['processing']}\n\nNext Steps:")
    for i, step in enumerate(result['next_steps'], 1):
        pdf.multi_cell(0, 8, f"{i}. {step}")

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# --- Eligibility Logic ---
def check_eb1_eligibility(criteria_data):
    # [Insert your full eligibility logic here — unchanged]
    # For brevity, I’ve omitted it here since you already have it.
    # Just paste your full `check_eb1_eligibility` function from your original code.
    pass

# --- Display Results ---
def display_results(result, criteria_data):
    status_html = f"""
    <div style="background-color: {result['color']}; padding: 10px; border-radius: 5px; color: white; text-align: center;"> 
        <h3 style="margin: 0; font-size: 20px;">{result['status']}</h3>  
        <p style="margin: 0; font-size: 14px;">Recommended Category: {result['category']}</p>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)
    st.subheader(result['title'])

    col1, col2 = st.columns(2)
    with col1:
        if result['score'] != 'N/A' and result['score'] != 'Met':
            st.metric("Score", result['score'])
    with col2:
        st.metric("Strength", result['strength'])

    st.markdown("**Assessment Details**")
    st.write(result['details'])

    st.markdown("**Processing Guidance**")
    st.info(result['processing'])

    st.markdown("**Recommended Next Steps**")
    for i, step in enumerate(result['next_steps'], 1):
        st.markdown(f"**{i}.** {step}")

    st.divider()
    st.warning("⚠️ This is a preliminary screening tool only and does NOT constitute legal advice.")

    # PDF Download Button
    pdf_bytes = generate_pdf(criteria_data, result)
    st.download_button(
        label="📄 Download Assessment as PDF",
        data=pdf_bytes,
        file_name="EB1_Eligibility_Report.pdf",
        mime="application/pdf"
    )

# --- Main App ---
def main():
    st.set_page_config(layout="wide", page_title="EB-1 Green Card Eligibility Screener")
    st.title("US EB-1 Green Card Eligibility Screener")
    st.caption("Evaluate your potential eligibility for EB-1A, EB-1B, or EB-1C categories.")
    st.divider()

    input_col, result_col = st.columns([1, 1])
    criteria_data = defaultdict(lambda: False)

    with input_col:
        st.subheader("1. Select Your Qualifications")

        with st.expander("🌟 EB-1A: Extraordinary Ability", expanded=False):
            criteria_data['major_award'] = st.checkbox("Major internationally recognized award")
            c1, c2 = st.columns(2)
            with c1:
                criteria_data['lesser_awards'] = st.checkbox("Lesser awards")
                criteria_data['membership'] = st.checkbox("Membership")
                criteria_data['publications'] = st.checkbox("Published material")
                criteria_data['judging'] = st.checkbox("Judging others")
                criteria_data['original_contributions'] = st.checkbox("Original contributions")
            with c2:
                criteria_data['authorship'] = st.checkbox("Authorship")
                criteria_data['performances'] = st.checkbox("Performances")
                criteria_data['high_salary'] = st.checkbox("High salary")
                criteria_data['commercial_success'] = st.checkbox("Commercial success")

        with st.expander("🔬 EB-1B: Outstanding Researcher/Professor", expanded=False):
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                criteria_data['experience'] = st.selectbox("Experience", ["<3_years", "3_years"])
            with col_b2:
                criteria_data['offer'] = st.selectbox("Job Offer", ["no", "yes"])
            with col_b3:
                criteria_data['tenure'] = st.selectbox("Tenure", ["no", "yes"])

            criteria_data['published_articles'] = st.checkbox("Published articles")
            criteria_data['judging_research'] = st.checkbox("Judged research")
            criteria_data['original_contributions_research'] = st.checkbox("Original research contributions")
            criteria_data['lesser_awards'] = criteria_data['lesser_awards'] or st.checkbox("Lesser awards (EB-1B)")
            criteria_data['membership'] = criteria_data['membership'] or st.checkbox("Membership (EB-1B)")

        with st.expander("🏢 EB-1C: Multinational Manager/Executive", expanded=False):
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                criteria_data['one_year_exp'] = st.selectbox("1+ year abroad", ["no", "yes"])
            with col_c2:
                criteria_data['managerial_role'] = st.selectbox("Managerial role", ["no", "yes"])
            with col_c3:
                criteria_data['transfer'] = st.selectbox("Transfer to US", ["no", "yes"])

    with result_col:
        st.subheader("2. Eligibility Assessment")
        if st.button("Run Assessment"):
            result = check_eb1_eligibility(criteria_data)
            display_results(result, criteria_data)

if __name__ == "__main__":
    main()
