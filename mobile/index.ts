import { registerRootComponent } from 'expo';
import { Platform } from 'react-native';

import App from './App';

// On web, the html/body background defaults to transparent (renders as black).
// Set it to the app's pale green so no black bleed-through appears on wide viewports
// or during page load.
if (Platform.OS === 'web') {
    const COLOR = '#F4F9F4'
    document.documentElement.style.backgroundColor = COLOR
    document.body.style.backgroundColor = COLOR
    document.body.style.margin = '0'
    document.body.style.padding = '0'
}

// registerRootComponent calls AppRegistry.registerComponent('main', () => App);
// It also ensures that whether you load the app in Expo Go or in a native build,
// the environment is set up appropriately
registerRootComponent(App);
