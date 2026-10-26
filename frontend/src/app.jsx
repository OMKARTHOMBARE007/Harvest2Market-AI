import { createContext, useContext, useState } from 'react';
import { Link, Navigate, Outlet, Route, Routes, useLocation } from 'react-router-dom';
import { Calculator, GitCompareArrows, LayoutDashboard, Sparkles, Store, UserRound } from 'lucide-react';
import api from './api.js';
import Navbar from './components/Navbar.jsx';
import Sidebar from './components/Sidebar.jsx';
import Home from './pages/Home.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Dashboard from './pages/Dashboard.jsx';
import MarketPrices from './pages/MarketPrices.jsx';
import PricePrediction from './pages/PricePrediction.jsx';
import ProfitCalculator from './pages/ProfitCalculator.jsx';
import MarketComparison from './pages/MarketComparison.jsx';
import Profile from './pages/Profile.jsx';
import AdminDashboard from './pages/AdminDashboard.jsx';
export const AuthContext=createContext(null); export const useAuth=()=>useContext(AuthContext);
export const money=(v)=>new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(Number(v||0));
export const navItems=[['/dashboard','Overview',LayoutDashboard],['/prices','Market prices',Store],['/prediction','Price estimate',Sparkles],['/calculator','Profit calculator',Calculator],['/comparison','Compare markets',GitCompareArrows],['/profile','My profile',UserRound]];
export default function App(){const[user,setUser]=useState(()=>{try{return JSON.parse(localStorage.getItem('h2m_user'))}catch{return null}});const[token,setToken]=useState(()=>localStorage.getItem('h2m_token'));const login=d=>{localStorage.setItem('h2m_token',d.access_token);localStorage.setItem('h2m_user',JSON.stringify(d.user));setToken(d.access_token);setUser(d.user)};const logout=()=>{localStorage.removeItem('h2m_token');localStorage.removeItem('h2m_user');setToken(null);setUser(null)};return <AuthContext.Provider value={{user,token,login,logout}}><Routes><Route path="/" element={<Home/>}/><Route path="/login" element={<Login onLogin={login}/>}/><Route path="/register" element={<Register onLogin={login}/>}/><Route element={<Protected/>}><Route path="/dashboard" element={<Dashboard/>}/><Route path="/prices" element={<MarketPrices/>}/><Route path="/prediction" element={<PricePrediction/>}/><Route path="/calculator" element={<ProfitCalculator/>}/><Route path="/comparison" element={<MarketComparison/>}/><Route path="/profile" element={<Profile/>}/><Route path="/admin" element={<AdminDashboard/>}/></Route><Route path="*" element={<Navigate to="/" replace/>}/></Routes></AuthContext.Provider>}
function Protected(){const{user,token}=useAuth();return user&&token?<Shell/>:<Navigate to="/login" replace/>}
function Shell(){const{user,logout}=useAuth();const[open,setOpen]=useState(false);const path=useLocation().pathname;const title=navItems.find(x=>x[0]===path)?.[1]||(path==='/admin'?'Admin overview':'Overview');return <div className="app-shell"><Sidebar user={user} onLogout={logout} open={open} items={navItems} onNavigate={()=>setOpen(false)}/><main className="main-area"><Navbar title={title} user={user} menuOpen={open} onToggleMenu={()=>setOpen(!open)}/><div className="page-content"><Outlet/></div></main></div>}
