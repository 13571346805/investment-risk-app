import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- 页面配置 ---
st.set_page_config(page_title="AI企业投资项目风险评估", layout="wide", page_icon="🛡️")

# --- 模拟AI模型逻辑 ---
def ai_risk_assessment_model(data):
    """
    模拟AI算法，根据输入指标计算风险评分 (0-100, 分数越高越优质)
    """
    weights = {
        'market_potential': 0.25,
        'team_strength': 0.20,
        'financial_health': 0.25,
        'tech_innovation': 0.15,
        'competition': 0.15
    }
    
    score = (
        data['market_potential'] * weights['market_potential'] +
        data['team_strength'] * weights['team_strength'] +
        data['financial_health'] * weights['financial_health'] +
        data['tech_innovation'] * weights['tech_innovation'] +
        data['competition'] * weights['competition']
    ) * 10  # 转为 0-100
    
    # 风险识别
    risks = []
    if data['financial_health'] < 5:
        risks.append("财务状况：现金流紧张/负债率偏高")
    if data['competition'] < 4:
        risks.append("市场竞争：红海市场，竞争极其激烈")
    if data['team_strength'] < 5:
        risks.append("团队风险：核心团队经验/稳定性不足")
    if data['market_potential'] > 8 and data['tech_innovation'] < 5:
        risks.append("技术匹配：市场大但壁垒低，易被复制")
    if data['financial_health'] < 3:
        risks.append("严重风险：财务基础极弱，谨慎介入")

    return round(score, 1), risks

def generate_investment_recommendation(score):
    if score >= 80:
        return "🟢 强烈建议投资", "success"
    elif score >= 65:
        return "🟡 建议跟进 & 深度尽调", "warning"
    elif score >= 50:
        return "🟠 谨慎观望 & 补齐短板", "warning"
    else:
        return "🔴 建议放弃 / 高风险", "error"

# --- 侧边栏 ---
st.sidebar.header("📊 项目数据录入")
st.sidebar.write("输入核心指标，AI自动评估")

with st.sidebar.form("project_form"):
    st.subheader("核心维度评分 (1–10分)")
    m_pot = st.slider("市场潜力", 1, 10, 7)
    t_str = st.slider("团队实力", 1, 10, 6)
    f_hea = st.slider("财务健康", 1, 10, 5)
    t_inn = st.slider("技术创新", 1, 10, 6)
    comp = st.slider("竞争优势", 1, 10, 5)
    
    submitted = st.form_submit_button("🚀 启动AI风险评估")

# --- 主界面 ---
st.title("🛡️ AI 企业投资项目风险评估系统")
st.markdown("---")

if submitted:
    # 数据封装
    input_data = {
        'market_potential': m_pot,
        'team_strength': t_str,
        'financial_health': f_hea,
        'tech_innovation': t_inn,
        'competition': comp
    }

    # AI 计算
    risk_score, risk_list = ai_risk_assessment_model(input_data)
    recommendation, rec_status = generate_investment_recommendation(risk_score)

    # 顶部指标卡片
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 AI 综合评分", f"{risk_score}/100")
    with col2:
        st.metric("🎯 投资建议", recommendation)
    with col3:
        st.metric("⚠️ 潜在风险", f"{len(risk_list)} 项")

    st.markdown("---")

    # 左右布局
    chart_col, text_col = st.columns([2, 1])

    with chart_col:
        st.subheader("📊 五维能力雷达图")
        categories = ['市场潜力', '团队实力', '财务健康', '技术创新', '竞争优势']
        fig = go.Figure(go.Scatterpolar(
            r=[m_pot, t_str, f_hea, t_inn, comp],
            theta=categories,
            fill='toself',
            name='项目评分'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,10])),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # 现金流预测
        st.subheader("💰 未来3年现金流预测")
        years = ["第1年", "第2年", "第3年"]
        base = f_hea * 12
        cash_flow = [base * 0.7, base * 1.4, base * 2.1]
        fig_bar = px.bar(
            x=years, y=cash_flow,
            labels={"x":"周期","y":"现金流(万元)"},
            color=years,
            color_discrete_sequence=["#3B82F6","#10B981","#6366F1"]
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with text_col:
        st.subheader("🚨 AI 风险诊断")
        if risk_list:
            for r in risk_list:
                st.error(r)
        else:
            st.success("✅ 未检测到结构性风险")

        st.divider()
        st.subheader("📝 AI 决策备忘录")
        best_idx = np.argmax([m_pot, t_str, f_hea, t_inn, comp])
        best_item = ['市场潜力','团队实力','财务健康','技术创新','竞争优势'][best_idx]
        
        report = f"""
**项目综合评分：{risk_score}**

✅ 优势项：**{best_item}** 表现突出
⚠️ 需关注：{len(risk_list)} 项风险点
🎯 建议：{recommendation}

> 本报告由AI模型生成，仅供投资决策参考。
        """
        st.markdown(report)

        # 下载报告
        st.download_button(
            label="📥 下载评估报告",
            data=report,
            file_name="投资风险评估报告.txt",
            mime="text/plain"
        )

else:
    # 初始状态
    st.info("👈 请在左侧填写项目指标，然后点击【启动AI风险评估】")
    
    st.subheader("💡 使用说明")
    st.write("""
    1. 在左侧滑动条输入 1–10 分评价
    2. 点击评估按钮
    3. 查看：综合评分、雷达图、风险点、投资建议
    """)

# --- 底部 ---
st.divider()
st.caption("⚡ AI投资风险评估系统 | 数据仅供参考 | 演示版本")