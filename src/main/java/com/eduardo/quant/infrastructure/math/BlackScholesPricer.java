package com.eduardo.quant.infrastructure.math;

import com.eduardo.quant.domain.model.EuropeanOption;
import com.eduardo.quant.domain.model.MarketSnapshot;
import com.eduardo.quant.domain.model.OptionType;
import com.eduardo.quant.domain.service.PricingModel;
import org.apache.commons.math3.distribution.NormalDistribution;

/**
 * Implementation of the Black-Scholes-Merton model for European Options.
 * Uses Apache Commons Math for high-precision Cumulative Distribution Function (CDF).
 */
public class BlackScholesPricer implements PricingModel {

    private static final NormalDistribution STANDARD_NORMAL = new NormalDistribution();

    @Override
    public double calculatePrice(EuropeanOption option, MarketSnapshot market) {
        double s0 = market.spotPrice();
        double k = option.strikePrice();
        double t = option.timeToMaturityYears();
        double r = market.riskFreeRate();
        double sigma = market.volatility();

        // Edge case: If time is 0, value is intrinsic value
        if (t <= 0) {
            return calculateIntrinsicValue(option, s0, k);
        }

        double d1 = (Math.log(s0 / k) + (r + 0.5 * Math.pow(sigma, 2)) * t) / (sigma * Math.sqrt(t));
        double d2 = d1 - sigma * Math.sqrt(t);

        if (option.type() == OptionType.CALL) {
            return s0 * STANDARD_NORMAL.cumulativeProbability(d1) -
                    k * Math.exp(-r * t) * STANDARD_NORMAL.cumulativeProbability(d2);
        } else {
            return k * Math.exp(-r * t) * STANDARD_NORMAL.cumulativeProbability(-d2) -
                    s0 * STANDARD_NORMAL.cumulativeProbability(-d1);
        }
    }

    private double calculateIntrinsicValue(EuropeanOption option, double s0, double k) {
        return (option.type() == OptionType.CALL)
                ? Math.max(0, s0 - k)
                : Math.max(0, k - s0);
    }
}