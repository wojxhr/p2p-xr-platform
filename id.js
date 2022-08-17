const { PeerServer } = require('peer');

const customGenerationFunction = () => (Math.random().toString(36) + '0000000000000000000').substr(2, 16);

const peerServer = PeerServer({
  port: 9100,
  path: '/signaling',
  generateClientId: customGenerationFunction
});