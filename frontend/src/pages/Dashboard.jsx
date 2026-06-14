import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from 'recharts'
import api from '../api'

const riskColor = { High:'#FAECE7', Medium:'#FAEEDA', Low:'#E1F5EE' }
const riskText  = { High:'#993C1D', Medium:'#854F0B', Low:'#0F6E56' }

export default function Dashboard() {
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(false)

  const [stats, setStats] = useState({
    total: 0,
    high: 0,
    medium: 0,
    low: 0
  })

  const nav = useNavigate()

  useEffect(() => {
    loadStudents()
    loadStats()
  }, [])

  const loadStudents = async () => {
    try {
      const res = await api.get('/students')
      setStudents(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const loadStats = async () => {
    try {
      const res = await api.get('/dashboard/stats')
      setStats(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const handleUpload = async (e) => {
      const file = e.target.files[0]
      if (!file) return

      setLoading(true)

      const form = new FormData()
      form.append('file', file)

      await api.post('/predict/upload', form)

      await loadStudents()
      await loadStats()

      setLoading(false)
  }

  const pieData = [
    {
      name: 'High',
      value: stats.high
    },
    {
      name: 'Medium',
      value: stats.medium
    },
    {
      name: 'Low',
      value: stats.low
    }
  ]

  const pieColors = [
    '#D85A30',
    '#D6A400',
    '#1D9E75'
  ]

  return (
    <div style={{padding:'2rem',maxWidth:860,margin:'0 auto'}}>
    
      <h2 style={{marginBottom:'1rem'}}>
        Student Risk Dashboard
      </h2>

      <div
        style={{
          display:'grid',
          gridTemplateColumns:'repeat(4,1fr)',
          gap:'12px',
          marginBottom:'2rem'
        }}
      >

        <div style={{
          padding:'16px',
          border:'1px solid #ddd',
          borderRadius:'10px'
        }}>
          <h3>Total</h3>
          <p>{stats.total}</p>
        </div>

        <div style={{
          padding:'16px',
          border:'1px solid #ddd',
          borderRadius:'10px'
        }}>
          <h3>High Risk</h3>
          <p>{stats.high}</p>
        </div>

        <div style={{
          padding:'16px',
          border:'1px solid #ddd',
          borderRadius:'10px'
        }}>
          <h3>Medium Risk</h3>
          <p>{stats.medium}</p>
        </div>

        <div style={{
          padding:'16px',
          border:'1px solid #ddd',
          borderRadius:'10px'
        }}>
          <h3>Low Risk</h3>
          <p>{stats.low}</p>
        </div>

      </div>

      <div
        style={{
          width:'100%',
          height:'300px',
          marginBottom:'2rem'
        }}
      >

        <ResponsiveContainer>

          <PieChart>

            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              outerRadius={100}
              label
            >
              {
                pieData.map((entry,index)=>(
                  <Cell
                    key={index}
                    fill={pieColors[index]}
                  />
                ))
              }
            </Pie>

            <Tooltip />

          </PieChart>

        </ResponsiveContainer>

      </div>
    
      <input type="file" accept=".csv" onChange={handleUpload}
        style={{marginBottom:'1.5rem'}} />
      {loading && <p>Analysing students...</p>}
      {students.length > 0 && (
        <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
          <thead>
            <tr style={{borderBottom:'0.5px solid #e0e0e0'}}>
              {['Name','Risk level','Risk score','Absences','Failures','Actions'].map(h=>
                <th key={h} style={{padding:'8px 12px',textAlign:'left',
                  fontWeight:500,color:'#666'}}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {students.map((s,i)=>(
              <tr key={i} onClick={() => nav(`/student/${s.id}`)}
                style={{cursor:'pointer',borderBottom:'0.5px solid #f0f0f0'}}>
                <td style={{padding:'8px 12px'}}>{s.name||'Student '+(i+1)}</td>
                <td style={{padding:'8px 12px'}}>
                  <span style={{background:riskColor[s.risk_level],
                    color:riskText[s.risk_level],padding:'2px 10px',
                    borderRadius:20,fontSize:11,fontWeight:500}}>
                    {s.risk_level}
                  </span>
                </td>
                <td style={{padding:'8px 12px'}}>{(s.risk_score*100).toFixed(0)}%</td>
                <td style={{padding:'8px 12px'}}>{s.absences??'—'}</td>
                <td style={{padding:'8px 12px'}}>{s.failures??'—'}</td>
                <td style={{padding:'8px 12px'}}>
                  <button
                    onClick={async (e) => {
                      e.stopPropagation()
                      if (
                        !window.confirm(
                          "Delete student?"
                        )
                      ) return
                      await api.delete(
                        `/students/${s.id}`
                      )
                      await loadStudents()
                    }}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}