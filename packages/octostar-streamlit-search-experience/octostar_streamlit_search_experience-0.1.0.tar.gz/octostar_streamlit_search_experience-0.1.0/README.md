# Octostar search experience streamlit component

Motivation to create a separate project for the component is to address problems with complex bidirectional components in Streamlit. The problem with the current search experience implementation is that Streamlit resets the state of the application each time a component returns a value what makes usage of conditions with UI components difficult.

Therefore, instead of spliting work with search experience into "trigger" and "get value" parts the easier way is to encapsulate work with the Octostar platform API inside a separate component what enables such component to set the value for Streamlit in whatever convenient way.

## Related resources

- https://streamlit-components-tutorial.netlify.app/introduction/;
