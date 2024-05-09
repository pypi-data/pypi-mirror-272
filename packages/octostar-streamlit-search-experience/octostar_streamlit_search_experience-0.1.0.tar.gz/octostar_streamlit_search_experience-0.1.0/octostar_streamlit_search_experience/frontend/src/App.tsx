import { desktopApi } from "@octostar/platform-api"
import { useEffect } from 'react'
import { ComponentProps, Streamlit, withStreamlitConnection } from "streamlit-component-lib"
import './App.css'

type ArgsType = {
  buttonText?: string;
}

function App(props: ComponentProps) {
  const {buttonText = 'Search'}: ArgsType = props.args;
  
  useEffect(() => {
    Streamlit.setFrameHeight()
  }, [])

  const handleSearchClick = async () => {
    const result = await desktopApi().searchXperience()

    console.log('search result', result)

    Streamlit.setComponentValue(result)
    Streamlit.setFrameHeight()
  }

  return (
    <button onClick={handleSearchClick} className="search-btn">
      {buttonText}
    </button>
  )
}

const ConnectedApp = withStreamlitConnection(App)

ConnectedApp.displayName = 'SearchExperience';

export default ConnectedApp
