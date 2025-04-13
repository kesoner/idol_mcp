import '@testing-library/jest-dom';

// Mock scrollIntoView
Element.prototype.scrollIntoView = function() {};

// Mock canvas
class MockCanvas {
  getContext() {
    return {
      fillRect: () => {},
      clearRect: () => {},
      getImageData: (x, y, w, h) => ({
        data: new Array(w * h * 4),
      }),
      putImageData: () => {},
      createImageData: () => [],
      setTransform: () => {},
      drawImage: () => {},
      save: () => {},
      restore: () => {},
      scale: () => {},
      rotate: () => {},
      translate: () => {},
      transform: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      stroke: () => {},
      fill: () => {},
    };
  }
}

// Mock WebGL context
const mockWebGLContext = {
  canvas: null,
  drawingBufferWidth: 0,
  drawingBufferHeight: 0,
  getExtension: () => null,
  getParameter: () => {},
  createBuffer: () => ({}),
  createFramebuffer: () => ({}),
  createProgram: () => ({}),
  createShader: () => ({}),
  createTexture: () => ({}),
  bindBuffer: () => {},
  bindFramebuffer: () => {},
  bindTexture: () => {},
  useProgram: () => {},
  enableVertexAttribArray: () => {},
  vertexAttribPointer: () => {},
  uniform1i: () => {},
  uniform1f: () => {},
  uniform2f: () => {},
  uniform3f: () => {},
  uniform4f: () => {},
  uniformMatrix4fv: () => {},
};

// Mock HTMLCanvasElement
global.HTMLCanvasElement.prototype.getContext = function(contextType) {
  if (contextType === '2d') {
    return new MockCanvas().getContext('2d');
  }
  if (contextType === 'webgl' || contextType === 'webgl2') {
    mockWebGLContext.canvas = this;
    return mockWebGLContext;
  }
  return null;
};

// Mock Live2D Cubism runtime
global.Live2DCubismCore = {
  version: () => '04.00.0000',
  CubismMatrix44: class {
    constructor() {
      this.elements = new Float32Array(16);
    }
  },
  CubismModel: class {
    constructor() {
      this.parameters = [];
      this.parts = [];
      this.drawables = [];
      this.canvasinfo = {};
    }
    getParameterCount() { return 0; }
    getParameterIds() { return []; }
    getParameterMinimumValues() { return []; }
    getParameterMaximumValues() { return []; }
    getParameterDefaultValues() { return []; }
    getParameterValues() { return []; }
    getPartCount() { return 0; }
    getPartIds() { return []; }
    getPartOpacities() { return []; }
    getDrawableCount() { return 0; }
    getDrawableIds() { return []; }
    getDrawableConstantFlags() { return []; }
    getDrawableDynamicFlags() { return []; }
    getDrawableTextureIndices() { return []; }
    getDrawableDrawOrders() { return []; }
    getDrawableRenderOrders() { return []; }
    getDrawableOpacities() { return []; }
    getDrawableMaskCounts() { return []; }
    getDrawableMasks() { return []; }
    getDrawableVertexCounts() { return []; }
    getDrawableVertexPositions() { return []; }
    getDrawableVertexUvs() { return []; }
    getDrawableIndexCounts() { return []; }
    getDrawableIndices() { return []; }
    update() {}
  },
}; 