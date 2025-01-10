import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';

const Welcome = () => {
  return (
    <Container className="mt-5 text-center">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="shadow-lg border-0">
            <Card.Body>
              <h1 className="display-4 mb-4">Welcome to Our Application!</h1>
              <p className="lead text-muted mb-4">
                Explore data, manage portals, and analyze taxonomy in one place. Get started now!
              </p>
              <div>
                <Button variant="primary" size="lg" className="me-3" as={Link} to={`/list`}>
                  Get Started
                </Button>
                <Button variant="outline-secondary" size="lg" as={Link} to={`/taxa`}>
                  Learn More
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Welcome;