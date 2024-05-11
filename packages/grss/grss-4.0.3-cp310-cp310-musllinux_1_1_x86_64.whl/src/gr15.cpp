#include "gr15.h"

/**
 * @param[in] propSim PropSimulation object for the integration.
 * @return real Initial timestep.
 */
real get_initial_timestep(PropSimulation *propSim){
    real dt0 = propSim->integParams.dtMin;
    if (propSim->integParams.dt0 != 0.0) {
        dt0 = fabs(propSim->integParams.dt0);
    }
    real span = fabs(propSim->integParams.tf - propSim->integParams.t0);
    if (span < dt0) {
        dt0 = span;
    }
    if (propSim->integParams.tf < propSim->integParams.t0) {
        dt0 *= -1.0;
    }
    return dt0;
}

/**
 * @param[in] b Matrix of interpolation coefficients.
 * @param[in] dim Dimension of the system (number of 2nd derivatives).
 * @param[out] g Matrix of interpolation coefficients.
 */
void update_g_with_b(const std::vector<std::vector<real>> &b, const size_t &dim, real *g) {
    for (size_t i = 0; i < dim; i++) {
        g[0*dim+i] = b[6][i]*dVec[15] + b[5][i]*dVec[10] + b[4][i]*dVec[6] + b[3][i]*dVec[3] + b[2][i]*dVec[1] + b[1][i]*dVec[0] + b[0][i];
        g[1*dim+i] = b[6][i]*dVec[16] + b[5][i]*dVec[11] + b[4][i]*dVec[7] + b[3][i]*dVec[4] + b[2][i]*dVec[2] + b[1][i];
        g[2*dim+i] = b[6][i]*dVec[17] + b[5][i]*dVec[12] + b[4][i]*dVec[8] + b[3][i]*dVec[5] + b[2][i];
        g[3*dim+i] = b[6][i]*dVec[18] + b[5][i]*dVec[13] + b[4][i]*dVec[9] + b[3][i];
        g[4*dim+i] = b[6][i]*dVec[19] + b[5][i]*dVec[14] + b[4][i];
        g[5*dim+i] = b[6][i]*dVec[20] + b[5][i];
        g[6*dim+i] = b[6][i];
    }
}

/**
 * @param[in] AccIntegArr Array of acceleration values at the nodes.
 * @param[in] hIdx Gauss-Radau node index.
 * @param[out] g Matrix of interpolation coefficients.
 * @param[out] bCompCoeffs Vector of compensated summation coefficients for computing the b-matrix.
 * @param[out] b Matrix of interpolation coefficients.
 * @param[in] dim Dimension of the system (number of 2nd derivatives).
 */
void compute_g_and_b(const std::vector<std::vector<real>> &AccIntegArr,
                     const size_t &hIdx, real *g, real *bCompCoeffs,
                     std::vector<std::vector<real>> &b, const size_t &dim) {
    switch (hIdx) {
        case 0:
            throw std::runtime_error("hIdx cannot be 0");
        case 1:
            for (size_t i = 0; i < dim; i++) {
                real dummy = 0;
                real temp = g[0*dim+i];
                real gVal = AccIntegArr[hIdx][i];
                comp_sum(-AccIntegArr[0][i], &gVal, &dummy);
                g[0*dim+i] = gVal/rVec[0];
                comp_sum(g[0*dim+i]-temp, &(b[0][i]), &(bCompCoeffs[0*dim+i]));
            }
            break;
        case 2:
            for (size_t i = 0; i < dim; i++) {
                real dummy = 0;
                real temp = g[1*dim+i];
                real gVal = AccIntegArr[hIdx][i];
                comp_sum(-AccIntegArr[0][i], &gVal, &dummy);
                g[1*dim+i] = (gVal/rVec[1] - g[0*dim+i])/rVec[2];
                temp = g[1*dim+i] - temp;
                comp_sum(temp*cVec[0], &(b[0][i]), &(bCompCoeffs[0*dim+i]));
                comp_sum(temp        , &(b[1][i]), &(bCompCoeffs[1*dim+i]));
            }
            break;
        case 3:
            for (size_t i = 0; i < dim; i++) {
                real dummy = 0;
                real temp = g[2*dim+i];
                real gVal = AccIntegArr[hIdx][i];
                comp_sum(-AccIntegArr[0][i], &gVal, &dummy);
                g[2*dim+i] = ((gVal/rVec[3] - g[0*dim+i])/rVec[4] - g[1*dim+i])/rVec[5];
                temp = g[2*dim+i] - temp;
                comp_sum(temp*cVec[1], &(b[0][i]), &(bCompCoeffs[0*dim+i]));
                comp_sum(temp*cVec[2], &(b[1][i]), &(bCompCoeffs[1*dim+i]));
                comp_sum(temp        , &(b[2][i]), &(bCompCoeffs[2*dim+i]));
            }
            break;
        case 4:
            for (size_t i = 0; i < dim; i++) {
                real dummy = 0;
                real temp = g[3*dim+i];
                real gVal = AccIntegArr[hIdx][i];
                comp_sum(-AccIntegArr[0][i], &gVal, &dummy);
                g[3*dim+i] = (((gVal/rVec[6] - g[0*dim+i])/rVec[7] - g[1*dim+i])/rVec[8] - g[2*dim+i])/rVec[9];
                temp = g[3*dim+i] - temp;
                comp_sum(temp*cVec[3], &(b[0][i]), &(bCompCoeffs[0*dim+i]));
                comp_sum(temp*cVec[4], &(b[1][i]), &(bCompCoeffs[1*dim+i]));
                comp_sum(temp*cVec[5], &(b[2][i]), &(bCompCoeffs[2*dim+i]));
                comp_sum(temp        , &(b[3][i]), &(bCompCoeffs[3*dim+i]));
            }
            break;
        case 5:
            for (size_t i = 0; i < dim; i++) {
                real dummy = 0;
                real temp = g[4*dim+i];
                real gVal = AccIntegArr[hIdx][i];
                comp_sum(-AccIntegArr[0][i], &gVal, &dummy);
                g[4*dim+i] = ((((gVal/rVec[10] - g[0*dim+i])/rVec[11] - g[1*dim+i])/rVec[12] - g[2*dim+i])/rVec[13] - g[3*dim+i])/rVec[14];
                temp = g[4*dim+i] - temp;
                comp_sum(temp*cVec[6], &(b[0][i]), &(bCompCoeffs[0*dim+i]));
                comp_sum(temp*cVec[7], &(b[1][i]), &(bCompCoeffs[1*dim+i]));
                comp_sum(temp*cVec[8], &(b[2][i]), &(bCompCoeffs[2*dim+i]));
                comp_sum(temp*cVec[9], &(b[3][i]), &(bCompCoeffs[3*dim+i]));
                comp_sum(temp        , &(b[4][i]), &(bCompCoeffs[4*dim+i]));
            }
            break;
        case 6:
            for (size_t i = 0; i < dim; i++) {
                real dummy = 0;
                real temp = g[5*dim+i];
                real gVal = AccIntegArr[hIdx][i];
                comp_sum(-AccIntegArr[0][i], &gVal, &dummy);
                g[5*dim+i] = (((((gVal/rVec[15] - g[0*dim+i])/rVec[16] - g[1*dim+i])/rVec[17] - g[2*dim+i])/rVec[18] - g[3*dim+i])/rVec[19] - g[4*dim+i])/rVec[20];
                temp = g[5*dim+i] - temp;
                comp_sum(temp*cVec[10], &(b[0][i]), &(bCompCoeffs[0*dim+i]));
                comp_sum(temp*cVec[11], &(b[1][i]), &(bCompCoeffs[1*dim+i]));
                comp_sum(temp*cVec[12], &(b[2][i]), &(bCompCoeffs[2*dim+i]));
                comp_sum(temp*cVec[13], &(b[3][i]), &(bCompCoeffs[3*dim+i]));
                comp_sum(temp*cVec[14], &(b[4][i]), &(bCompCoeffs[4*dim+i]));
                comp_sum(temp         , &(b[5][i]), &(bCompCoeffs[5*dim+i]));
            }
            break;
        case 7:
            for (size_t i = 0; i < dim; i++) {
                real dummy = 0;
                real temp = g[6*dim+i];
                real gVal = AccIntegArr[hIdx][i];
                comp_sum(-AccIntegArr[0][i], &gVal, &dummy);
                g[6*dim+i] = ((((((gVal/rVec[21] - g[0*dim+i])/rVec[22] - g[1*dim+i])/rVec[23] - g[2*dim+i])/rVec[24] - g[3*dim+i])/rVec[25] - g[4*dim+i])/rVec[26] - g[5*dim+i])/rVec[27];
                temp = g[6*dim+i] - temp;
                comp_sum(temp*cVec[15], &(b[0][i]), &(bCompCoeffs[0*dim+i]));
                comp_sum(temp*cVec[16], &(b[1][i]), &(bCompCoeffs[1*dim+i]));
                comp_sum(temp*cVec[17], &(b[2][i]), &(bCompCoeffs[2*dim+i]));
                comp_sum(temp*cVec[18], &(b[3][i]), &(bCompCoeffs[3*dim+i]));
                comp_sum(temp*cVec[19], &(b[4][i]), &(bCompCoeffs[4*dim+i]));
                comp_sum(temp*cVec[20], &(b[5][i]), &(bCompCoeffs[5*dim+i]));
                comp_sum(temp         , &(b[6][i]), &(bCompCoeffs[6*dim+i]));
            }
            break;
        default:
            throw std::runtime_error("hIdx is out of range");
    }
}

/**
 * @param[inout] b Matrix of interpolation coefficients.
 * @param[inout] e Refinement matrix.
 * @param[in] dtRatio Ratio of the required timestep to the previous timestep.
 * @param[in] dim Dimension of the system (number of 2nd derivatives).
 */
void refine_b(std::vector<std::vector<real>> &b,
              real *e, const real &dtRatio,
              const size_t &dim) {
    std::vector<std::vector<real>> bDiff(7, std::vector<real>(dim, 0.0L));
    for (size_t i = 0; i < dim; i++){
        bDiff[0][i] = b[0][i] - e[0*dim+i];
        bDiff[1][i] = b[1][i] - e[1*dim+i];
        bDiff[2][i] = b[2][i] - e[2*dim+i];
        bDiff[3][i] = b[3][i] - e[3*dim+i];
        bDiff[4][i] = b[4][i] - e[4*dim+i];
        bDiff[5][i] = b[5][i] - e[5*dim+i];
        bDiff[6][i] = b[6][i] - e[6*dim+i];
    }

    real q = dtRatio;
    real q2 = q * q;
    real q3 = q2 * q;
    real q4 = q2 * q2;
    real q5 = q2 * q3;
    real q6 = q3 * q3;
    real q7 = q2 * q5;

    for (size_t i = 0; i < dim; i++) {
        e[0*dim+i] = q  * (b[6][i] * 7.0  + b[5][i] * 6.0  + b[4][i] * 5.0  + b[3][i] * 4.0 + b[2][i] * 3.0 + b[1][i] * 2.0 + b[0][i]);
        e[1*dim+i] = q2 * (b[6][i] * 21.0 + b[5][i] * 15.0 + b[4][i] * 10.0 + b[3][i] * 6.0 + b[2][i] * 3.0 + b[1][i]);
        e[2*dim+i] = q3 * (b[6][i] * 35.0 + b[5][i] * 20.0 + b[4][i] * 10.0 + b[3][i] * 4.0 + b[2][i]);
        e[3*dim+i] = q4 * (b[6][i] * 35.0 + b[5][i] * 15.0 + b[4][i] * 5.0  + b[3][i]);
        e[4*dim+i] = q5 * (b[6][i] * 21.0 + b[5][i] * 6.0  + b[4][i]);
        e[5*dim+i] = q6 * (b[6][i] * 7.0  + b[5][i]);
        e[6*dim+i] = q7 * (b[6][i]);
    }

    for (size_t i = 0; i < dim; i++) {
        b[0][i] = e[0*dim+i] + bDiff[0][i];
        b[1][i] = e[1*dim+i] + bDiff[1][i];
        b[2][i] = e[2*dim+i] + bDiff[2][i];
        b[3][i] = e[3*dim+i] + bDiff[3][i];
        b[4][i] = e[4*dim+i] + bDiff[4][i];
        b[5][i] = e[5*dim+i] + bDiff[5][i];
        b[6][i] = e[6*dim+i] + bDiff[6][i];
    }
}

/**
 * @param[in] propSim PropSimulation object for the integration.
 * @param[in] t Current time.
 * @param[out] tNextEvent Time of the next event.
 * @param[out] nextEventIdx Index of the next event.
 * @param[in] xInteg Vector of integrated states after the current timestep.
 */
void check_and_apply_events(PropSimulation *propSim, const real &t,
                            real &tNextEvent, size_t &nextEventIdx,
                            std::vector<real> &xInteg) {
    while (nextEventIdx < propSim->events.size() && t == tNextEvent) {
        // apply events for the state just reached by the integrator
        real propDir;
        if (propSim->integParams.t0 < propSim->integParams.tf) {
            propDir = 1.0L;
        } else {
            propDir = -1.0L;
        }
        propSim->events[nextEventIdx].apply(t, xInteg, propDir);
        // update next event index and time
        nextEventIdx++;
        if (nextEventIdx < propSim->events.size()) {
            tNextEvent = propSim->events[nextEventIdx].t;
        } else {
            tNextEvent = propSim->integParams.tf;
        }
    }
}

/**
 * @brief Compute the 7th root of a number.
 * 
 * @param[in] num Number to compute the 7th root of.
 * @return real 7th root of the number.
 */
static real root7(real num){
    real fac = 1.0;
    if (num<1e-7){
        fac = 0.1;
        num *= 1e7;
    }
    if (num>1e2){
        fac = 10.0;
        num *= 1e-7;
    }
    real root = 1.0;
    for (size_t i = 0; i < 20; i++) {
        root += (num/(root*root*root*root*root*root)-root)/7.0;
    }
    return fac*root;
}

// /**
//  * @brief Get the next timestep based on the old IAS15 adaptive timestep criterion.
//  * 
//  * @param[in] propSim PropSimulation object for the integration.
//  * @param[in] dt Current timestep.
//  * @param[in] accIntegArr7Max Maximum acceleration value at the last node.
//  * @param[in] b Matrix of interpolation coefficients.
//  * @return real Next timestep.
//  */
// static real get_adaptive_timestep_old(PropSimulation *propSim, const real &dt,
//                                       const real &accIntegArr7Max,
//                                       const std::vector<std::vector<real>> &b) {
//     real b6Max;
//     vabs_max(b[6], b6Max);
//     real relError = b6Max / accIntegArr7Max;
//     real dtReq;
//     if (std::isnormal(relError)) {
//         dtReq = root7(propSim->integParams.tolInteg/relError)*dt;
//     } else {
//         dtReq = dt/propSim->integParams.dtChangeFactor;
//     }
//     return dtReq;
// }

/**
 * @brief Get the next timestep based on the new IAS15 adaptive timestep criterion.
 * 
 * @param[in] propSim PropSimulation object for the integration.
 * @param[in] dt Current timestep.
 * @param[in] accInteg0 Vector of acceleration values at the current timestep.
 * @param[in] b Matrix of interpolation coefficients.
 * @return real Next timestep.
 */
static real get_adaptive_timestep(PropSimulation *propSim, const real &dt,
                                  const std::vector<real> &accInteg0,
                                  const std::vector<std::vector<real>> &b) {
    real minTimescale2 = 1e300L;
    size_t startb = 0;
    for (size_t i = 0; i < propSim->integParams.nInteg; i++){
        real y2 = 0.0L;
        real y3 = 0.0L;
        real y4 = 0.0L;
        for (size_t j = 0; j < 3; j++){
            const size_t k = startb+j;
            real temp = accInteg0[k] + b[0][k] + b[1][k] + b[2][k] + b[3][k] + b[4][k] + b[5][k] + b[6][k];
            y2 += temp*temp;
            temp = b[0][k] + 2.0L*b[1][k] + 3.0L*b[2][k] + 4.0L*b[3][k] + 5.0L*b[4][k] + 6.0L*b[5][k] + 7.0L*b[6][k];
            y3 += temp*temp;
            temp = 2.0L*b[1][k] + 6.0L*b[2][k] + 12.0L*b[3][k] + 20.0L*b[4][k] + 30.0L*b[5][k] + 42.0L*b[6][k];
            y4 += temp*temp;
            real timescale2 = 2.0L*y2/(y3+sqrt(y4*y2));
            if (std::isnormal(timescale2) && timescale2 < minTimescale2){
                minTimescale2 = timescale2;
            }
        }
    }
    real dtReq;
    if (std::isnormal(minTimescale2)){
        // Numerical factor below is for relating the epsilon in original IAS15 to the 
        // eta in the new IAS15 stepping from https://arxiv.org/pdf/2401.02849.pdf
        dtReq = sqrt(minTimescale2) * root7(propSim->integParams.tolInteg*5040.0) * dt;
    }else{
        dtReq = dt/propSim->integParams.dtChangeFactor;
    }
    return dtReq;
}

/**
 * @param[inout] propSim PropSimulation object for the integration.
 */
void gr15(PropSimulation *propSim) {
    if (!std::isfinite(propSim->t)) {
        throw std::runtime_error("t is not finite");
    }
    for (size_t i = 0; i < propSim->xInteg.size(); i++) {
        if (!std::isfinite(propSim->xInteg[i])) {
            throw std::runtime_error("xInteg is not finite");
        }
    }
    real t = propSim->t;
    std::vector<real> xInteg0 = propSim->xInteg;
    size_t nh = 8;
    size_t dim = propSim->integParams.n2Derivs;
    real dt = get_initial_timestep(propSim);
    propSim->integParams.timestepCounter = 0;
    std::vector<real> xInteg(propSim->xInteg.size(), 0.0);
    std::vector<real> xIntegCompCoeffs(propSim->xInteg.size(), 0.0);
    std::vector<std::vector<real> > bOld(7, std::vector<real>(dim, 0.0));
    std::vector<std::vector<real> > b(7, std::vector<real>(dim, 0.0));
    real *bCompCoeffs = new real [7 * dim];
    memset(bCompCoeffs, 0.0, 7 * dim * sizeof(real));
    real *g = new real[7 * dim];
    memset(g, 0.0, 7 * dim * sizeof(real));
    real *e = new real[7 * dim];
    memset(e, 0.0, 7 * dim * sizeof(real));
    std::vector<std::vector<real> > accIntegArr(nh,
                                                std::vector<real>(dim, 0.0));
    real *b6Tilde = new real[dim];
    memset(b6Tilde, 0.0, dim * sizeof(real));
    real b6TildeMax, accIntegArr7Max;
    real dtReq;
    real tNextEvent = propSim->integParams.tf;
    size_t nextEventIdx = 0;
    if (t == propSim->integParams.t0) {
        nextEventIdx = 0;
    }
    if (propSim->events.size() != 0) {
        tNextEvent = propSim->events[0].t;
    }
    check_and_apply_events(propSim, t, tNextEvent, nextEventIdx, xInteg0);
    if ((propSim->integParams.tf > propSim->integParams.t0 &&
         t + dt > tNextEvent) ||
        (propSim->integParams.tf < propSim->integParams.t0 &&
         t + dt < tNextEvent)) {
        dt = tNextEvent - t;
    }
    std::vector<real> accInteg0 = get_state_der(t, xInteg0, propSim);
    std::vector<real> accIntegNext = std::vector<real>(accInteg0.size(), 0.0);
    propSim->interpParams.tStack.push_back(t);
    propSim->interpParams.xIntegStack.push_back(xInteg0);
    size_t PCmaxIter = 12;
    int keepStepping = 1;
    int oneStepDone = 0;
    if (propSim->integParams.t0 == propSim->integParams.tf) {
        keepStepping = 0;
    }
    while (keepStepping) {
        t = propSim->t;
        xInteg0 = propSim->xInteg;
        oneStepDone = 0;
        update_g_with_b(b, dim, g);
        while (!oneStepDone) {
            real PCerr = 1.0/propSim->integParams.tolPC;
            real PCerrPrev = PCerr + 1.0;
            accIntegArr[0] = accInteg0;
            size_t PCIter = 0;
            while (true) {
                if (PCerr < propSim->integParams.tolPC) {
                    break;
                }
                if (PCerr > PCerrPrev && PCIter > 2) {
                    break;
                }
                if (PCIter > PCmaxIter) {
                    break;
                }
                PCerrPrev = PCerr;
                PCIter++;
                for (size_t hIdx = 1; hIdx < nh; hIdx++) {
                    approx_xInteg(xInteg0, accInteg0, dt, hVec[hIdx], b,
                                  propSim->integBodies, xInteg, xIntegCompCoeffs);
                    accIntegArr[hIdx] = get_state_der(
                        t + hVec[hIdx] * dt, xInteg, propSim);
                    compute_g_and_b(accIntegArr, hIdx, g, bCompCoeffs, b, dim);
                }
                for (size_t i = 0; i < dim; i++) {
                    b6Tilde[i] = b[6][i] - bOld[6][i];
                }
                vabs_max(b6Tilde, dim, b6TildeMax);
                vabs_max(accIntegArr[7], accIntegArr7Max);
                PCerr = b6TildeMax / accIntegArr7Max;
                bOld = b;
            }
            if (propSim->integParams.adaptiveTimestep) {
                // dtReq = get_adaptive_timestep_old(propSim, dt, accIntegArr7Max, b);
                dtReq = get_adaptive_timestep(propSim, dt, accInteg0, b);
            } else {
                dtReq = dt;
            }
            if (fabs(dtReq) < propSim->integParams.dtMin) {
                dtReq = copysign(propSim->integParams.dtMin, dtReq);
            }
            if (fabs(dtReq/dt) < propSim->integParams.dtChangeFactor) {
                // std::cout << "Restarting next while loop at time t = " << t
                //           << " with dt = " << dtReq << " instead of " << dt
                //           << std::endl;
                dt = dtReq;
                continue;
            }
            // accept step
            if (dtReq / dt > 1.0 / propSim->integParams.dtChangeFactor) {
                dtReq = dt / propSim->integParams.dtChangeFactor;
            }
            propSim->interpParams.bStack.push_back(b);
            propSim->interpParams.accIntegStack.push_back(accInteg0);
            if (propSim->tEval.size() != propSim->xIntegEval.size()) {
                interpolate_on_the_fly(propSim, t, dt);
            }
            approx_xInteg(xInteg0, accInteg0, dt, 1.0, b,
                        propSim->integBodies, xInteg, xIntegCompCoeffs);
            t += dt;
            propSim->t = t;
            accInteg0 = get_state_der(t, xInteg, propSim);
            check_and_apply_events(propSim, t, tNextEvent, nextEventIdx,
                                    xInteg);
            propSim->xInteg = xInteg;
            propSim->interpParams.tStack.push_back(t);
            propSim->interpParams.xIntegStack.push_back(xInteg);
            propSim->integParams.timestepCounter++;
            if (propSim->integParams.timestepCounter > 1) {
                refine_b(b, e, dtReq / dt, dim);
            }
            check_ca_or_impact(propSim, t-dt, xInteg0, t, xInteg);
            if ((propSim->integParams.tf > propSim->integParams.t0 &&
                    t >= propSim->integParams.tf) ||
                (propSim->integParams.tf < propSim->integParams.t0 &&
                    t <= propSim->integParams.tf)) {
                keepStepping = 0;
            }
            dt = dtReq;
            if ((propSim->integParams.tf > propSim->integParams.t0 &&
                 t + dt > tNextEvent) ||
                (propSim->integParams.tf < propSim->integParams.t0 &&
                 t + dt < tNextEvent)) {
                dt = tNextEvent - t;
            }
            oneStepDone = 1;
        }
    }
    propSim->interpParams.bStack.push_back(b);
    propSim->interpParams.accIntegStack.push_back(accInteg0);
    delete[] bCompCoeffs;
    delete[] g;
    delete[] e;
    delete[] b6Tilde;
}
