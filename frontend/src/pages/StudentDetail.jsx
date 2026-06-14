import { useParams } from 'react-router-dom'
import { useState, useEffect } from 'react'
import api from '../api'
import { BarChart, Bar, XAxis, YAxis, Tooltip,
         Cell, ResponsiveContainer } from 'recharts'

export default function StudentDetail() {

  const { id } = useParams()

  const [s, setStudent] = useState(null)

  useEffect(() => {
    loadStudent()
  }, [])

  const loadStudent = async () => {
    try {
      const res = await api.get(`/students/${id}`)
      setStudent(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  if (!s) return <p>Loading...</p>

  const shap = s.shap_factors || []
  const chartData = shap.map(f => ({
    name: f.feature,
    value: Math.abs(f.shap_value),
    positive: f.impact === 'increases'
  }))

  const riskCol = {High:'#993C1D',Medium:'#854F0B',Low:'#0F6E56'}

  return (
    <div style={{padding:'2rem',maxWidth:700,margin:'0 auto'}}>
      <h2 style={{marginBottom:4}}>{s.name || 'Student'}</h2>
      <div
        style={{
          marginTop:'1rem',
          padding:'1rem',
          border:'1px solid #ddd',
          borderRadius:'10px'
        }}
      >
        <h3>Student Information</h3>

        <p>
          <strong>Absences:</strong> {s.absences}
        </p>

        <p>
          <strong>Failures:</strong> {s.failures}
        </p>

        <p>
          <strong>Study Time:</strong> {s.studytime}
        </p>

        <p>
          <strong>Created:</strong> {s.created_at}
        </p>

      </div>
      <span style={{fontSize:13,color:riskCol[s.risk_level],fontWeight:500}}>
        {s.risk_level} risk — {(s.risk_score*100).toFixed(0)}% probability
      </span>

      <h3 style={{marginTop:'1.5rem',marginBottom:'0.75rem',fontSize:15}}>
        Why is this student flagged?
      </h3>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={chartData} layout="vertical">
          <XAxis type="number" hide />
          <YAxis type="category" dataKey="name" width={90} fontSize={12}/>
          <Tooltip formatter={v=>[v.toFixed(3),'SHAP value']} />
          <Bar dataKey="value" radius={[0,4,4,0]}>
            {chartData.map((d,i)=>(
              <Cell key={i} fill={d.positive ? '#D85A30' : '#1D9E75'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p style={{fontSize:12,color:'#888',marginTop:4}}>
        Red = increases risk · Green = decreases risk
      </p>

      <h3 style={{marginTop:'1.5rem',marginBottom:'0.75rem',fontSize:15}}>
        Recommended interventions
      </h3>
      {(s.interventions||[]).map((a,i)=>(
        <div
          key={i}
          style={{
            padding:'10px 14px',
            border:'0.5px solid #e0e0e0',
            borderRadius:8,
            marginBottom:8,
            fontSize:13
          }}
        >

          <div
            style={{
              display:'flex',
              justifyContent:'space-between'
            }}
          >

            <span>
              {a.action}
            </span>

            <span
              style={{
                background:a.applied
                  ? '#E1F5EE'
                  : '#FAEEDA',
                color:a.applied
                  ? '#0F6E56'
                  : '#854F0B',
                padding:'2px 8px',
                borderRadius:'20px',
                fontSize:'11px'
              }}
            >
              <div>

                <span
                  style={{
                    marginRight:'10px'
                  }}
                >
                  {a.applied
                    ? 'Completed'
                    : 'Pending'}
                </span>

                {!a.applied && (

                  <button
                    onClick={async ()=>{

                      await api.patch(
                        `/interventions/${a.id}/complete`
                      )

                      window.location.reload()

                    }}
                  >
                    Complete
                  </button>

                )}

              </div>
            </span>

          </div>

        </div>
      ))}
    </div>
  )
}