 module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      webpackConfig.module.rules = webpackConfig.module.rules.map(rule => {
        if (rule.oneOf) {
          rule.oneOf = rule.oneOf.map(innerRule => {
            if (
              innerRule.loader &&
              innerRule.loader.includes('source-map-loader')
            ) {
              // Add exclude for node_modules here explicitly
              return {
               ...innerRule,
                exclude: /node_modules/,
              };
            }
            return innerRule;
          });
        }
        return rule;
      });
      return webpackConfig;
    },
  },
};
