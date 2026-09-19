import { useEffect, useState } from 'react'

function App() {
    const [backendStatus, setBackendStatus] = useState('Checking...')
    const [dashboard, setDashboard] = useState(null)
    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/health')
        .then((response) => response.json())
        .then((data) => {
            setBackendStatus(data.status)
        })
            .catch(() => {
                setBackendStatus('Backend unavailable')
                })
        fetch('http://127.0.0.1:8000/api/dashboard')
        .then((response) => response.json())
            .then((data) => {
                setDashboard(data)
            })
        }, [])


    return (
        <div>
            <h1>Fitness Analytics Platform</h1>

            <h2> Backend Status </h2>
            <p>{backendStatus}</p>

            <h2>Today's Nutrition</h2>

            <div>

                <p>{dashboard?.calories} / {dashboard?.calorie_goal}</p>
                <p>Protein: 0g / 150g</p>
                <p>Carbs: 0g / 300g</p>
                <p>Fat: 0g / 70g</p>
            </div>

            <h2>Today's Workout</h2>

            <p>No workout logged yet.</p>
        </div>

  )
}

export default App