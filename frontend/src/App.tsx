import { useEffect, useState } from 'react'

type Dashboard = {
    calories: number
    calorie_goal: number
    protein: number
    protein_goal: number
    carbs: number
    carbs_goal: number
    fat: number
    fat_goal: number
}
function App() {
    const [backendStatus, setBackendStatus] = useState('Checking...')
    const [dashboard, setDashboard] = useState<Dashboard | null>(null)
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

                <p>Calories: {dashboard?.calories} / {dashboard?.calorie_goal}</p>
                <p>Protein: {dashboard?.protein}g / {dashboard?.protein_goal}g</p>
                <p>Carbs: {dashboard?.carbs}g / {dashboard?.carbs_goal}g</p>
                <p>Fat: {dashboard?.fat}g / {dashboard?.fat_goal}g</p>
            </div>

            <h2>Today's Workout</h2>

            <p>No workout logged yet.</p>
        </div>

  )
}

export default App