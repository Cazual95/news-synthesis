import React, {useState} from "react";
import HttpClient from "../HttpClient";
import {Box, Button, Theme, Text, TextField} from "@radix-ui/themes";
import {json} from "react-router-dom";

const LoginPage = () => {
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [loginMessage, setLoginMessage] = useState<string>("")

    async function login(event: React.MouseEvent) {
        console.log('Button Pressed')
        const resp = await HttpClient.post('http://localhost:5000/auth/login',
            {email, password})
        console.log(resp.data.error)

        if (resp.status == 200) {
            window.location.href = '/'
        } else {
            setLoginMessage(resp.data.error)
        }
    }

    return <Theme appearance="dark">
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh'}}>
            <Box>
                <h1>Please Login</h1>
                <form>
                    <p>{loginMessage}</p>
                    <div><Text as="label">Email: </Text>
                        <TextField.Input placeholder="Enter your email" value={email}
                                         onChange={(e) => setEmail(e.target.value)}/>
                    </div>
                    <div><Text as="label">Password: </Text>
                        <TextField.Input type={'password'} placeholder="Enter your password" value={password}
                                         onChange={(e) => setPassword(e.target.value)}/>
                    </div>
                    <div>
                        <Button type={'button'} onClick={(event) => login(event)}>Submit</Button>
                    </div>
                </form>
            </Box>
        </div>
    </Theme>
}

export default LoginPage