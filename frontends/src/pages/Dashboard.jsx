import React, { useEffect, useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const [students, setStudents] = useState([]);
    const [form, setForm] = useState({ name: '', email: '', course: '' });
    const [editingId, setEditingId] = useState(null);
    const navigate = useNavigate();

    const fetchStudents = async () => {
        try {
            const res = await api.get('/students');
            setStudents(res.data);
        } catch (err) {
            console.error("Failed to fetch students");
            if (err.response && err.response.status === 401) logout();
        }
    };

    useEffect(() => {
        fetchStudents();
    }, []);

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingId) {
                await api.put(`/students/${editingId}`, form);
            } else {
                await api.post('/students', form);
            }
            setForm({ name: '', email: '', course: '' });
            setEditingId(null);
            fetchStudents();
        } catch (err) {
            console.error(err);
        }
    };

    const handleEdit = (student) => {
        setForm({ name: student.name, email: student.email, course: student.course });
        setEditingId(student._id);
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure?")) return;
        try {
            await api.delete(`/students/${id}`);
            fetchStudents();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
            <header className="glass-card" style={{ padding: '1rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ margin: 0, color: '#4f46e5' }}>Student Management</h1>
                <button onClick={logout} className="btn btn-danger">Logout</button>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
                <div className="glass-card" style={{ padding: '1.5rem', height: 'fit-content' }}>
                    <h3 style={{ marginTop: 0, marginBottom: '1.5rem' }}>{editingId ? 'Edit Student' : 'Add New Student'}</h3>
                    <form onSubmit={handleSubmit}>
                        <input
                            className="form-input"
                            placeholder="Full Name"
                            value={form.name}
                            onChange={e => setForm({ ...form, name: e.target.value })}
                            required
                        />
                        <input
                            className="form-input"
                            placeholder="Email Address"
                            value={form.email}
                            onChange={e => setForm({ ...form, email: e.target.value })}
                            required
                        />
                        <input
                            className="form-input"
                            placeholder="Course"
                            value={form.course}
                            onChange={e => setForm({ ...form, course: e.target.value })}
                            required
                        />
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                                {editingId ? 'Update' : 'Add'}
                            </button>
                            {editingId && (
                                <button
                                    type="button"
                                    onClick={() => { setEditingId(null); setForm({ name: '', email: '', course: '' }) }}
                                    className="btn"
                                    style={{ background: '#9ca3af', color: 'white' }}
                                >
                                    Cancel
                                </button>
                            )}
                        </div>
                    </form>
                </div>

                <div className="glass-card" style={{ padding: '1.5rem', overflowX: 'auto' }}>
                    <h3 style={{ marginTop: 0 }}>Student List</h3>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Course</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {students.map(student => (
                                <tr key={student._id}>
                                    <td>{student.name}</td>
                                    <td>{student.email}</td>
                                    <td>{student.course}</td>
                                    <td style={{ display: 'flex', gap: '0.5rem' }}>
                                        <button onClick={() => handleEdit(student)} className="btn btn-warning" style={{ padding: '0.5rem 1rem' }}>Edit</button>
                                        <button onClick={() => handleDelete(student._id)} className="btn btn-danger" style={{ padding: '0.5rem 1rem' }}>Delete</button>
                                    </td>
                                </tr>
                            ))}
                            {students.length === 0 && (
                                <tr>
                                    <td colSpan="4" style={{ textAlign: 'center', color: '#6b7280' }}>No students found</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
