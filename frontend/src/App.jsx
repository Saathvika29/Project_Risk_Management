
import { useState } from "react";
import {
  LayoutDashboard, ClipboardList, ShieldAlert, ListOrdered,
  Network, Lightbulb, Bell, Search, Menu, Activity,
  FolderKanban, AlertTriangle, CheckCircle2, ArrowUpRight,
  Plus, RefreshCw
} from "lucide-react";

import {
  ResponsiveContainer, PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from "recharts";

import "./App.css";

const API = "http://127.0.0.1:8000/api/";

const navigation = [
  { name: "Overview", icon: LayoutDashboard },
  { name: "Project Assessment", icon: ClipboardList },
  { name: "Risk Severity", icon: ShieldAlert },
  { name: "Risk Prioritization", icon: ListOrdered },
  { name: "Interdependencies", icon: Network },
  { name: "Recommendations", icon: Lightbulb }
];

const pieData = [
  { name: "Critical", value: 4, color: "#DC6262" },
  { name: "High", value: 8, color: "#E9A23B" },
  { name: "Medium", value: 12, color: "#3978C5" },
  { name: "Low", value: 6, color: "#40A78B" }
];

const barData = [
  { name: "Technical", risks: 12 },
  { name: "Financial", risks: 8 },
  { name: "Operational", risks: 6 },
  { name: "Compliance", risks: 4 }
];

// Demo records for the prioritization and interdependency modules.
// Replace these with database records when database integration is added.
const sampleRisks = [
  { "Risk ID": "R01", "Risk Name": "Technical Failure", Impact: 9, Probability: 90 },
  { "Risk ID": "R02", "Risk Name": "Budget Overrun", Impact: 8, Probability: 70 },
  { "Risk ID": "R03", "Risk Name": "Resource Shortage", Impact: 6, Probability: 50 },
  { "Risk ID": "R04", "Risk Name": "Schedule Delay", Impact: 4, Probability: 30 }
];

const sampleRelationships = [
  ["Technical Failure", "Schedule Delay"],
  ["Schedule Delay", "Budget Overrun"],
  ["Resource Shortage", "Schedule Delay"],
  ["Technical Failure", "Budget Overrun"]
];

async function postAPI(endpoint, payload) {
  const response = await fetch(`${API}${endpoint}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data === "object" ? JSON.stringify(data) : "API request failed"
    );
  }

  return data;
}

function App() {
  const [activePage, setActivePage] = useState("Overview");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const [form, setForm] = useState({
    project_industry: "Healthcare",
    project_duration: 17,
    percentage_of_completion: 64,
    initial_budget: 715937,
    cost_variance: -108820,
    scope_creep: 5,
    technical_complexity: 2,
    operational_efficiency: 4,
    budget_changes: 5,
    regulations_impact: 4,
    deviations_from_strategic_goals: 2,
    market_fluctuations: 5,
    reputational_impact: 3,
    environmental_impact: 1,
    legal_challenges: 2,
    security_threats: 4,
    supply_chain_disruptions: 5,
    hr_issues: 5,
    schedule_changes: 3,
    schedule_variance: -2,
    stakeholder_issues: 5,
    stakeholder_engagement_level: 3,
    stakeholder_influence_level: 1,
    external_dependencies: 3,
    economic_conditions: 0,
    quality_issues: 0
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [severityResult, setSeverityResult] = useState(null);
  const [severityForm, setSeverityForm] = useState({
    impact: 9,
    probability: 90
  });

  const [priorityResult, setPriorityResult] = useState(null);
  const [interdependencyResult, setInterdependencyResult] = useState(null);
  const [recommendationResult, setRecommendationResult] = useState(null);

  const [pageLoading, setPageLoading] = useState(false);
  const [pageError, setPageError] = useState("");

  const updateForm = (e) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      [name]: name === "project_industry" ? value : Number(value)
    });
  };

  const updateSeverityForm = (e) => {
    const { name, value } = e.target;
    setSeverityForm({
      ...severityForm,
      [name]: Number(value)
    });
  };

  const runPrediction = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const data = await postAPI("predict", form);
      setPrediction(data.predictions);

      // Keep the severity page ready with the latest prediction.
      setSeverityForm({
        impact: data.predictions.risk_impact,
        probability: data.predictions.risk_probability
      });
      setSeverityResult(null);
      setRecommendationResult(null);
    } catch (err) {
      setError(err.message || "Unable to connect to Django API.");
    } finally {
      setLoading(false);
    }
  };

  const runSeverity = async (e) => {
    e.preventDefault();
    setPageLoading(true);
    setPageError("");
    setSeverityResult(null);

    try {
      const data = await postAPI("severity", severityForm);
      setSeverityResult(data.result);
    } catch (err) {
      setPageError(err.message);
    } finally {
      setPageLoading(false);
    }
  };

  const runPrioritization = async () => {
    setPageLoading(true);
    setPageError("");
    setPriorityResult(null);

    try {
      const data = await postAPI("prioritize", {
        risks: sampleRisks
      });
      setPriorityResult(data.result);
    } catch (err) {
      setPageError(err.message);
    } finally {
      setPageLoading(false);
    }
  };

  const runInterdependencies = async () => {
    setPageLoading(true);
    setPageError("");
    setInterdependencyResult(null);

    const risks = sampleRisks.map((risk) => {
      const score = risk.Impact * risk.Probability / 100;
      let severity = "Low";

      if (score > 6) severity = "Critical";
      else if (score > 4) severity = "High";
      else if (score > 2) severity = "Medium";

      return {
        "Risk Name": risk["Risk Name"],
        Severity: severity,
        "Risk Score": Number(score.toFixed(2))
      };
    });

    try {
      const data = await postAPI("interdependencies", {
        risks,
        relationships: sampleRelationships
      });
      setInterdependencyResult(data.result);
    } catch (err) {
      setPageError(err.message);
    } finally {
      setPageLoading(false);
    }
  };

  const runRecommendations = async () => {
    setPageLoading(true);
    setPageError("");
    setRecommendationResult(null);

    if (!prediction) {
      setPageError("Please run a Project Assessment first to generate ML predictions.");
      setPageLoading(false);
      return;
    }

    try {
      const data = await postAPI("recommendations", {
        risk_name: "Predicted Project Risk",
        risk_type: prediction.risk_type,
        impact: prediction.risk_impact,
        probability: prediction.risk_probability
      });
      setRecommendationResult(data.result);
    } catch (err) {
      setPageError(err.message);
    } finally {
      setPageLoading(false);
    }
  };

  const runButton = (label, action) => (
    <button
      className="primary-btn"
      onClick={action}
      disabled={pageLoading}
    >
      {pageLoading ? (
        <> <RefreshCw size={16} /> Processing... </>
      ) : (
        <> <Activity size={16} /> {label} </>
      )}
    </button>
  );

  const resultPanel = (title, children) => (
    <div className="panel feature-result">
      <h3>{title}</h3>
      {children}
    </div>
  );

  const errorPanel = pageError && (
    <div className="error-box">{pageError}</div>
  );

  const renderOverview = () => (
    <>
      <div className="welcome">
        <div>
          <p className="eyebrow">PROJECT ANALYTICS</p>
          <h1>Dashboard Overview</h1>
          <p>Monitor, analyse and manage project risks intelligently.</p>
        </div>
        <button className="primary-btn" onClick={() => setActivePage("Project Assessment")}>
          <Plus size={17} /> New Assessment
        </button>
      </div>

      <div className="stats-grid">
        {[
          { title: "Total Projects", value: "24", icon: FolderKanban, change: "Illustrative data" },
          { title: "Identified Risks", value: "30", icon: Activity, change: "Illustrative data" },
          { title: "Critical Risks", value: "04", icon: AlertTriangle, change: "Illustrative data" },
          { title: "Resolved Risks", value: "18", icon: CheckCircle2, change: "Illustrative data" }
        ].map((item) => {
          const Icon = item.icon;
          return (
            <div className="stat-card" key={item.title}>
              <div className="stat-top">
                <span>{item.title}</span>
                <Icon size={19} />
              </div>
              <h2>{item.value}</h2>
              <p>{item.change}</p>
            </div>
          );
        })}
      </div>

      <div className="charts-grid">
        <div className="panel">
          <h3>Risk Distribution</h3>
          <p className="panel-subtitle">Illustrative overview data</p>
          <div className="chart">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={65} outerRadius={95} paddingAngle={4}>
                  {pieData.map((item) => <Cell key={item.name} fill={item.color} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="legend">
            {pieData.map((item) => (
              <span key={item.name}>
                <i style={{ background: item.color }} /> {item.name}
              </span>
            ))}
          </div>
        </div>

        <div className="panel">
          <h3>Risks by Category</h3>
          <p className="panel-subtitle">Illustrative overview data</p>
          <div className="chart">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="risks" fill="#3978C5" radius={[5, 5, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="panel">
        <h3>Quick Actions</h3>
        <p className="panel-subtitle">Start analysing your project risks</p>
        <button className="secondary-btn" onClick={() => setActivePage("Project Assessment")}>
          Create a new project risk assessment <ArrowUpRight size={16} />
        </button>
      </div>
    </>
  );

  const renderAssessment = () => (
    <>
      <div className="welcome">
        <div>
          <p className="eyebrow">MACHINE LEARNING</p>
          <h1>Project Risk Assessment</h1>
          <p>Enter project parameters to generate intelligent risk predictions.</p>
        </div>
      </div>

      <form className="panel assessment-form" onSubmit={runPrediction}>
        <h3>Project Information</h3>
        <div className="form-grid">
          <label>
            Project Industry
            <select name="project_industry" value={form.project_industry} onChange={updateForm}>
              {["Healthcare", "Construction", "IT", "Finance", "Manufacturing"].map((v) => (
                <option key={v}>{v}</option>
              ))}
            </select>
          </label>

          {Object.entries(form)
            .filter(([key]) => key !== "project_industry")
            .map(([key, value]) => (
              <label key={key}>
                {key.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                <input
                  type="number"
                  name={key}
                  value={value}
                  onChange={updateForm}
                  required
                />
              </label>
            ))}
        </div>

        <button className="primary-btn submit-btn" disabled={loading}>
          {loading ? "Analysing Project..." : "Generate Risk Prediction"}
        </button>
      </form>

      {error && <div className="error-box">{error}</div>}

      {prediction && (
        <div className="panel prediction-panel">
          <p className="eyebrow">ML MODEL RESULTS</p>
          <h2>Risk Prediction Results</h2>
          <div className="result-grid">
            <div><span>Risk Type</span><strong>{prediction.risk_type}</strong></div>
            <div><span>Impact</span><strong>{prediction.risk_impact}</strong></div>
            <div><span>Probability</span><strong>{prediction.risk_probability}%</strong></div>
            <div><span>Response Plan</span><strong>{prediction.risk_response_plan}</strong></div>
            <div><span>Risk Score</span><strong>{prediction.risk_severity["Risk Score"]}</strong></div>
            <div><span>Severity</span><strong className="critical">{prediction.risk_severity.Severity}</strong></div>
          </div>
          <p className="panel-subtitle">
            You can use this prediction in the Risk Severity and Recommendations modules.
          </p>
        </div>
      )}
    </>
  );

  const renderSeverity = () => (
    <>
      <div className="welcome">
        <div>
          <p className="eyebrow">RISK ANALYSIS</p>
          <h1>Risk Severity Analysis</h1>
          <p>Calculate risk severity using impact and probability.</p>
        </div>
      </div>

      <form className="panel assessment-form" onSubmit={runSeverity}>
        <h3>Risk Parameters</h3>
        {prediction && (
          <p className="panel-subtitle">
            Latest ML prediction is available. You can use it or change the values.
          </p>
        )}
        <div className="form-grid">
          <label>
            Risk Impact (1–10)
            <input type="number" min="1" max="10" step="0.01" name="impact" value={severityForm.impact} onChange={updateSeverityForm} required />
          </label>
          <label>
            Risk Probability (0–100)
            <input type="number" min="0" max="100" step="0.01" name="probability" value={severityForm.probability} onChange={updateSeverityForm} required />
          </label>
        </div>
        <button className="primary-btn submit-btn" disabled={pageLoading}>
          {pageLoading ? "Calculating..." : "Analyse Risk Severity"}
        </button>
      </form>

      {errorPanel}

      {severityResult && resultPanel("Risk Severity Result", (
        <div className="result-grid">
          <div><span>Impact</span><strong>{severityResult.Impact}</strong></div>
          <div><span>Probability</span><strong>{severityResult.Probability}%</strong></div>
          <div><span>Risk Score</span><strong>{severityResult["Risk Score"]}</strong></div>
          <div><span>Severity Level</span><strong className="critical">{severityResult.Severity}</strong></div>
        </div>
      ))}
    </>
  );

  const renderPrioritization = () => (
    <>
      <div className="welcome">
        <div>
          <p className="eyebrow">RISK RANKING</p>
          <h1>Risk Prioritization</h1>
          <p>Rank identified risks according to their risk scores.</p>
        </div>
      </div>

      <div className="panel">
        <h3>Risk Records</h3>
        <p className="panel-subtitle">Sample risk records for demonstration</p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr><th>Risk ID</th><th>Risk Name</th><th>Impact</th><th>Probability</th></tr>
            </thead>
            <tbody>
              {sampleRisks.map((risk) => (
                <tr key={risk["Risk ID"]}>
                  <td>{risk["Risk ID"]}</td>
                  <td>{risk["Risk Name"]}</td>
                  <td>{risk.Impact}</td>
                  <td>{risk.Probability}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {runButton("Prioritize Risks", runPrioritization)}
      </div>

      {errorPanel}

      {priorityResult && resultPanel("Prioritized Risk List", (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                {Object.keys(priorityResult[0] || {}).map((key) => <th key={key}>{key}</th>)}
              </tr>
            </thead>
            <tbody>
              {priorityResult.map((risk, index) => (
                <tr key={index}>
                  {Object.values(risk).map((value, i) => <td key={i}>{String(value)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </>
  );

  const renderInterdependencies = () => (
    <>
      <div className="welcome">
        <div>
          <p className="eyebrow">RISK RELATIONSHIP ANALYSIS</p>
          <h1>Risk Interdependency Analysis</h1>
          <p>Identify connections between risks and find highly connected risks.</p>
        </div>
      </div>

      <div className="panel">
        <h3>Risk Relationships</h3>
        <p className="panel-subtitle">Demonstration relationships defined for this example</p>
        <ul className="relationship-list">
          {sampleRelationships.map(([source, target], index) => (
            <li key={index}>{source} <ArrowUpRight size={15} /> {target}</li>
          ))}
        </ul>
        {runButton("Analyse Interdependencies", runInterdependencies)}
      </div>

      {errorPanel}

      {interdependencyResult && (
        <>
          {resultPanel("Most Connected Risk", (
            <h2>{interdependencyResult.most_connected_risk || "Not available"}</h2>
          ))}

          {resultPanel("Interdependency Analysis", (
            <>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Risk Name</th>
                      <th>Degree Centrality</th>
                      <th>Incoming</th>
                      <th>Outgoing</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(interdependencyResult.risk_analysis || []).map((risk, index) => (
                      <tr key={index}>
                        <td>{risk.risk_name}</td>
                        <td>{risk.degree_centrality}</td>
                        <td>{risk.incoming_connections}</td>
                        <td>{risk.outgoing_connections}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="panel-subtitle">
                Relationships shown here are predefined demonstration connections, not proof of causation.
              </p>
            </>
          ))}
        </>
      )}
    </>
  );

  const renderRecommendations = () => (
    <>
      <div className="welcome">
        <div>
          <p className="eyebrow">INTELLIGENT DECISION SUPPORT</p>
          <h1>Risk Recommendations</h1>
          <p>Generate suggested risk response actions based on predicted risk details.</p>
        </div>
      </div>

      <div className="panel">
        <h3>Generate Recommendations</h3>
        {prediction ? (
          <>
            <p className="panel-subtitle">
              Current prediction: {prediction.risk_type} risk, impact {prediction.risk_impact},
              probability {prediction.risk_probability}%.
            </p>
            {runButton("Generate Recommendations", runRecommendations)}
          </>
        ) : (
          <>
            <p className="panel-subtitle">
              Run a Project Assessment first. Recommendations use the ML-predicted risk type, impact and probability.
            </p>
            <button className="primary-btn" onClick={() => setActivePage("Project Assessment")}>
              Go to Project Assessment <ArrowUpRight size={16} />
            </button>
          </>
        )}
      </div>

      {errorPanel}

      {recommendationResult && resultPanel("Recommended Risk Response Actions", (
        <>
          <div className="result-grid">
            <div><span>Risk Type</span><strong>{recommendationResult["Risk Type"]}</strong></div>
            <div><span>Impact</span><strong>{recommendationResult.Impact}</strong></div>
            <div><span>Probability</span><strong>{recommendationResult.Probability}%</strong></div>
            <div><span>Risk Score</span><strong>{recommendationResult["Risk Score"]}</strong></div>
            <div><span>Severity</span><strong className="critical">{recommendationResult.Severity}</strong></div>
          </div>
          <h3>Suggested Actions</h3>
          <ol className="recommendation-list">
            {(recommendationResult.Recommendations || []).map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ol>
        </>
      ))}
    </>
  );

  const pageRenderers = {
    "Overview": renderOverview,
    "Project Assessment": renderAssessment,
    "Risk Severity": renderSeverity,
    "Risk Prioritization": renderPrioritization,
    "Interdependencies": renderInterdependencies,
    "Recommendations": renderRecommendations
  };

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "" : "collapsed"}`}>
        <div className="brand">
          <div className="brand-icon">R</div>
          {sidebarOpen && <span>Risk<span className="brand-light">Wise</span></span>}
        </div>

        <p className="nav-label">{sidebarOpen ? "WORKSPACE" : ""}</p>

        {navigation.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.name}
              className={`nav-item ${activePage === item.name ? "active" : ""}`}
              onClick={() => {
                setActivePage(item.name);
                setPageError("");
              }}
              title={item.name}
            >
              <Icon size={19} />
              {sidebarOpen && <span>{item.name}</span>}
            </button>
          );
        })}

        <div className="sidebar-bottom">
          <div className="profile-avatar">SG</div>
          {sidebarOpen && <div><strong>Project Team</strong><small>Administrator</small></div>}
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <button className="icon-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
            <Menu size={21} />
          </button>
          <div className="breadcrumb">Workspace / <strong>{activePage}</strong></div>
          <div className="top-actions">
            <button className="icon-btn"><Search size={19} /></button>
            <button className="icon-btn"><Bell size={19} /></button>
            <div className="top-avatar">SG</div>
          </div>
        </header>

        <div className="page-content">
          {pageRenderers[activePage]()}
        </div>
      </main>
    </div>
  );
}

export default App;

