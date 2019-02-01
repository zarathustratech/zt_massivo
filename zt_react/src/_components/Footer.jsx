import React from 'react';


const Footer = () => (
  <footer className="footer">
    <div className="container">
      <div className="row align-items-center flex-row-reverse">
        <div className="col-auto ml-lg-auto">
          <div className="row align-items-center">
            <div className="col-auto">
              <ul className="list-inline list-inline-dots mb-0">
                <li className="list-inline-item">
                  <a href="https://nplx.com">
                    Terms of service
                  </a>
                </li>
                <li className="list-inline-item">
                  <a href="https://nplx.com">
                    Privacy policy
                  </a>
                </li>
              </ul>
            </div>
            <div className="col-auto">
              <a href="https://nplx.com" className="btn btn-outline-primary btn-sm">
                Contact us
              </a>
            </div>
          </div>
        </div>
        <div className="col-12 col-lg-auto mt-3 mt-lg-0 text-center">
          Copyright © 2018
          <a href="https://nplx.com">
            Zarathustra Technologies
          </a>
          . All rights reserved.
        </div>
      </div>
    </div>
  </footer>
);

export default Footer;
