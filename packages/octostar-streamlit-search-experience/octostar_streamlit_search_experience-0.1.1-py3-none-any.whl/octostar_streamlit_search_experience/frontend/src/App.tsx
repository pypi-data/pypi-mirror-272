import { desktopApi } from "@octostar/platform-api"
import { useEffect } from 'react'
import { ComponentProps, Streamlit, withStreamlitConnection } from "streamlit-component-lib"
import './App.css'

type ArgsType = {
  params?: {
    button_text?: string;
  };
};

function App(props: ComponentProps) {
  const args: ArgsType = props.args;
  const { button_text = "Search" } = args.params || {};

  useEffect(() => {
    Streamlit.setFrameHeight();
  }, []);

  const handleSearchClick = async () => {
    const result = await desktopApi().searchXperience();

    console.log("search result", result);

    Streamlit.setComponentValue(result);
    Streamlit.setFrameHeight();
  };

  return (
    <button onClick={handleSearchClick} className="search-btn">
      {button_text}
    </button>
  );
}

const ConnectedApp = withStreamlitConnection(App)

ConnectedApp.displayName = 'SearchExperience';

export default ConnectedApp
