from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('manager_id', sa.Integer(), nullable=True),
        sa.Column('team', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('client', sa.String(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    op.create_table('resources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('skills', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('capacity_hours_per_week', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_id'), 'resources', ['id'], unique=False)
    op.create_table('ai_prompt_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('template_text', sa.String(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_prompt_templates_id'), 'ai_prompt_templates', ['id'], unique=False)
    op.create_table('allocations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('allocation_percent', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_allocations_id'), 'allocations', ['id'], unique=False)
    op.create_table('timesheets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.Column('week_start_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('approved_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_timesheets_id'), 'timesheets', ['id'], unique=False)
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('actor_user_id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('diff_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['actor_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_table('timesheet_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timesheet_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('task', sa.String(), nullable=False),
        sa.Column('hours', sa.Float(), nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['timesheet_id'], ['timesheets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_timesheet_entries_id'), 'timesheet_entries', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_timesheet_entries_id'), table_name='timesheet_entries')
    op.drop_table('timesheet_entries')
    op.drop_index(op.f('ix_audit_logs_id'), table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index(op.f('ix_timesheets_id'), table_name='timesheets')
    op.drop_table('timesheets')
    op.drop_index(op.f('ix_allocations_id'), table_name='allocations')
    op.drop_table('allocations')
    op.drop_index(op.f('ix_ai_prompt_templates_id'), table_name='ai_prompt_templates')
    op.drop_table('ai_prompt_templates')
    op.drop_index(op.f('ix_resources_id'), table_name='resources')
    op.drop_table('resources')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
