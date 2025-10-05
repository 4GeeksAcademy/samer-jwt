import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/authContext';

export const Private = () => {
    const { user, logout, loading } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (!loading && !user) {
            navigate('/login');
        }
    }, [user, loading, navigate]);

    if (loading) {
        return (
            <div className="container mt-5 text-center">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Cargando...</span>
                </div>
            </div>
        );
    }

    if (!user) {
        return null;
    }

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div>
            <nav className="navbar navbar-dark bg-primary">
                <div className="container-fluid">
                    <span className="navbar-brand mb-0 h1">Área Privada</span>
                    <button
                        className="btn btn-danger"
                        onClick={handleLogout}
                    >
                        Cerrar Sesión
                    </button>
                </div>
            </nav>

            <div className="container mt-5">
                <div className="card shadow">
                    <div className="card-body">
                        <h2 className="card-title">Bienvenido a tu área privada</h2>
                        <div className="alert alert-info mt-4">
                            <p className="mb-1"><strong>Email:</strong> {user.email}</p>
                            <p className="mb-0"><strong>ID:</strong> {user.id}</p>
                        </div>
                        <p className="text-muted mt-3">
                            Esta es una página protegida. Solo usuarios autenticados pueden acceder.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};