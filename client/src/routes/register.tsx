import {useState} from "react";

const RegisterPage = () => {
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")

    return <div>
        <h1>Please Register Your Account</h1>
        <form>
            <label>Email:</label>
            <input type={'string'} value={email} onChange={(e) => setEmail(e.target.value)}/>
            <label>Password:</label>
            <input type={'string'} value={password} onChange={(e) => setPassword(e.target.value)}/>
        </form>
    </div>
}

export default RegisterPage