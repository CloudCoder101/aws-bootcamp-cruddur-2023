import './App.css';
import { Amplify } from 'aws-amplify';

import HomeFeedPage from './pages/HomeFeedPage';
import UserFeedPage from './pages/UserFeedPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';
import React from 'react';

import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";

Amplify.configure({
  Auth: {
    Cognito: {
      region: process.env.REACT_APP_AWS_REGION,
      userPoolId: process.env.REACT_APP_COGNITO_USER_POOL_ID,
      userPoolClientId: process.env.REACT_APP_COGNITO_CLIENT_ID,    
    }
  }
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomeFeedPage />
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />
  },
  {
    path: "/messages/@:handle",
    element: <MessageGroupPage />
  },
  {
    path: "/signup",
    element: <SignupPage />
  },
  {
    path: "/signin",
    element: <SigninPage />
  },

  {
    path: "/confirm/:email", 
    element: <ConfirmationPage /> 
  },

  {
    path: "/forgot",
    element: <RecoverPage />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;